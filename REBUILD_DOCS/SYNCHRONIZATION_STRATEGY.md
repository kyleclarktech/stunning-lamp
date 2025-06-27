# Event-Driven Synchronization Strategy

## Overview

This document outlines the event-driven synchronization strategy that keeps all system components in sync without complex coordination logic. By emitting events for all significant changes, the system maintains consistency across modules, the graph database, and external integrations.

## Core Event System

### Event Structure

```typescript
interface SystemEvent {
  id: string;                    // Unique event ID
  type: EventType;              // Event category
  timestamp: Date;              // When it occurred
  source: string;               // Module that emitted it
  payload: any;                 // Event-specific data
  metadata?: EventMetadata;     // Optional context
}

enum EventType {
  // Code changes
  'code.modified',
  'code.deleted',
  'refactor.complete',
  
  // Data changes
  'entity.created',
  'entity.updated',
  'entity.deleted',
  
  // PM events
  'project.created',
  'task.assigned',
  'task.completed',
  'bottleneck.detected',
  
  // System events
  'schema.updated',
  'touchpoint.added',
  'module.loaded'
}
```

## Event Flows

### 1. Code Change Synchronization

When code is modified, touchpoints and documentation stay in sync:

```typescript
// Claude Code detects file save
on('file.saved', async (file: string) => {
  // Extract touchpoints from modified file
  const touchpoints = await extractTouchpoints(file);
  
  // Update touchpoint index
  await updateTouchpointIndex(file, touchpoints);
  
  // Emit event for other modules
  emit({
    type: 'touchpoint.updated',
    source: 'claude-code',
    payload: { file, touchpoints }
  });
});

// Context Manager receives update
on('touchpoint.updated', async (event) => {
  // Invalidate cached contexts containing this file
  await contextCache.invalidate(event.payload.file);
  
  // Update search indices
  await searchIndex.update(event.payload.touchpoints);
});
```

### 2. Graph Data Synchronization

All data changes flow through events:

```typescript
// PM Assistant creates a project
async function createProject(description: string) {
  // Create in graph
  const project = await graphExecutor.execute(createProjectCypher);
  
  // Emit event
  emit({
    type: 'project.created',
    source: '@pm-assistant',
    payload: { 
      projectId: project.id,
      description,
      createdBy: currentUser
    }
  });
  
  return project;
}

// Other modules can react
on('project.created', async (event) => {
  // Notification service
  await notifyTeam(event.payload);
  
  // Analytics service
  await trackProjectCreation(event.payload);
  
  // Integration service
  await syncToExternalTools(event.payload);
});
```

### 3. Schema Evolution Events

When the graph schema changes:

```typescript
// Schema change detected
on('schema.updated', async (event) => {
  const { addedTypes, modifiedTypes, deletedTypes } = event.payload;
  
  // Query Engine updates its knowledge
  if (queryEngine) {
    await queryEngine.refreshSchema({
      added: addedTypes,
      modified: modifiedTypes,
      deleted: deletedTypes
    });
  }
  
  // Update documentation
  await generateSchemaDoc(event.payload);
  
  // Validate existing queries still work
  await validateStoredQueries(event.payload);
});
```

## Event Bus Implementation

### Simple Event Bus

```typescript
class SystemEventBus {
  private handlers = new Map<EventType, Set<EventHandler>>();
  private eventLog: SystemEvent[] = [];
  
  // Subscribe to events
  on(type: EventType, handler: EventHandler): Unsubscribe {
    if (!this.handlers.has(type)) {
      this.handlers.set(type, new Set());
    }
    
    this.handlers.get(type)!.add(handler);
    
    // Return unsubscribe function
    return () => {
      this.handlers.get(type)?.delete(handler);
    };
  }
  
  // Emit event to all handlers
  async emit(event: Omit<SystemEvent, 'id' | 'timestamp'>): Promise<void> {
    const fullEvent: SystemEvent = {
      ...event,
      id: generateId(),
      timestamp: new Date()
    };
    
    // Log event
    this.eventLog.push(fullEvent);
    
    // Notify handlers
    const handlers = this.handlers.get(event.type) || new Set();
    
    // Execute handlers in parallel
    await Promise.all(
      Array.from(handlers).map(handler => 
        handler(fullEvent).catch(error => 
          console.error(`Handler error for ${event.type}:`, error)
        )
      )
    );
  }
  
  // Query event history
  getEvents(filter?: EventFilter): SystemEvent[] {
    return this.eventLog.filter(event => 
      !filter || matchesFilter(event, filter)
    );
  }
}

// Global instance
export const eventBus = new SystemEventBus();
```

## Module Integration

### How Modules Subscribe

Each module declares its event interests:

```typescript
// In @pm-assistant/index.ts
export class PMAssistant implements Module {
  initialize() {
    // Subscribe to relevant events
    eventBus.on('task.completed', this.handleTaskComplete.bind(this));
    eventBus.on('entity.updated', this.handleEntityUpdate.bind(this));
    eventBus.on('schema.updated', this.refreshSchema.bind(this));
  }
  
  private async handleTaskComplete(event: SystemEvent) {
    const { taskId, completedBy } = event.payload;
    
    // Update project progress
    await this.updateProjectProgress(taskId);
    
    // Check for newly unblocked tasks
    const unblocked = await this.findUnblockedTasks(taskId);
    
    // Emit events for unblocked tasks
    for (const task of unblocked) {
      eventBus.emit({
        type: 'task.unblocked',
        source: '@pm-assistant',
        payload: { taskId: task.id, unblockedBy: taskId }
      });
    }
  }
}
```

## Claude Code Integration

### CLAUDE.md Configuration

```markdown
## Event Handling

This project uses event-driven synchronization. When modifying code:

1. File changes trigger touchpoint updates automatically
2. Graph changes emit events for system-wide sync
3. Schema changes propagate to all modules

Available events:
- `code.modified` - When you save a file
- `entity.created/updated/deleted` - When graph data changes
- `touchpoint.updated` - When code annotations change

Example:
```typescript
// Your changes will emit events automatically
// @touchpoint new-feature
export function newFeature() {
  // This will trigger touchpoint.updated event
}
```
```

## Benefits

### 1. Loose Coupling
- Modules don't need to know about each other
- Easy to add new modules that listen to events
- Can remove modules without breaking others

### 2. Automatic Consistency
- No manual sync code needed
- Events ensure all parts stay updated
- Single source of truth (graph + events)

### 3. Audit Trail
- Event log provides complete history
- Easy debugging with event replay
- Can reconstruct state from events

### 4. Extensibility
- New integrations just subscribe to events
- External tools can be notified
- Easy to add new event types

## Event Patterns

### 1. Command Events
Trigger actions in other modules:
```typescript
eventBus.emit({
  type: 'task.assign',
  source: '@pm-assistant',
  payload: { taskId, personId }
});
```

### 2. Notification Events
Inform about completed actions:
```typescript
eventBus.emit({
  type: 'task.assigned',
  source: '@graph-executor',
  payload: { taskId, personId, assignedAt }
});
```

### 3. System Events
Infrastructure-level changes:
```typescript
eventBus.emit({
  type: 'module.loaded',
  source: '@module-loader',
  payload: { moduleId, capabilities }
});
```

## Error Handling

```typescript
// Events shouldn't crash the system
class ResilientEventBus extends SystemEventBus {
  async emit(event: SystemEvent): Promise<void> {
    try {
      await super.emit(event);
    } catch (error) {
      // Log but don't throw
      console.error('Event emission failed:', error);
      
      // Emit error event
      await super.emit({
        type: 'event.failed',
        source: 'event-bus',
        payload: { 
          originalEvent: event,
          error: error.message 
        }
      });
    }
  }
}
```

## Testing Event Flows

```typescript
describe('Event Synchronization', () => {
  let eventBus: SystemEventBus;
  
  beforeEach(() => {
    eventBus = new SystemEventBus();
  });
  
  test('task completion triggers progress update', async () => {
    const projectUpdated = jest.fn();
    eventBus.on('project.progress.updated', projectUpdated);
    
    // Emit task completion
    await eventBus.emit({
      type: 'task.completed',
      source: 'test',
      payload: { taskId: 'task-1', projectId: 'proj-1' }
    });
    
    // Verify cascade
    expect(projectUpdated).toHaveBeenCalledWith(
      expect.objectContaining({
        payload: expect.objectContaining({
          projectId: 'proj-1'
        })
      })
    );
  });
});
```

## Performance Considerations

### 1. Event Batching
```typescript
class BatchedEventBus extends SystemEventBus {
  private batch: SystemEvent[] = [];
  private batchTimer?: NodeJS.Timeout;
  
  async emit(event: SystemEvent): Promise<void> {
    this.batch.push(event);
    
    if (!this.batchTimer) {
      this.batchTimer = setTimeout(() => this.flush(), 10);
    }
  }
  
  private async flush() {
    const events = [...this.batch];
    this.batch = [];
    this.batchTimer = undefined;
    
    // Process batch
    await Promise.all(events.map(e => super.emit(e)));
  }
}
```

### 2. Selective Subscription
```typescript
// Only subscribe to specific entity types
eventBus.on('entity.updated', async (event) => {
  if (event.payload.entityType !== 'Task') return;
  
  // Handle task updates only
  await handleTaskUpdate(event.payload);
});
```

## Summary

Event-driven synchronization provides a simple, scalable way to keep all system components in sync. By emitting events for all significant changes and having modules subscribe to relevant events, we achieve:

- Loose coupling between modules
- Automatic consistency across the system
- Easy extensibility for new features
- Built-in audit trail
- Simple integration with external systems

The event bus becomes the nervous system of the application, carrying signals between components without them needing direct knowledge of each other.
