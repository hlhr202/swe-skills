# Architect Implement Flow

```mermaid
flowchart TD
    Start([User requests implementation or resume]) --> Load[Read implement-track-protocol.md]
    Load --> SetupCheck[Verify required Architect context and tracks directory]
    SetupCheck -->|Missing required context| NotSetup[Halt and suggest setup or propose]
    SetupCheck -->|Ready| Parse[Parse tracks.md]
    Parse --> Select{Can target track be selected uniquely?}
    Select -->|No| AskTrack[Ask user to choose a track]
    Select -->|Yes| Resolve[Resolve safe track directory from registry link]
    AskTrack --> Resolve
    Resolve --> TrackFiles[Read spec.md, plan.md, metadata.json, workflow, product, guidelines, and tech stack]
    TrackFiles -->|Missing track file| HaltIncomplete[Halt and suggest setup recovery or track inspection]
    TrackFiles -->|Ready| ModeAsk[Ask implementation mode]
    ModeAsk -->|Manual| MarkTrack[Mark track and metadata in progress]
    ModeAsk -->|Auto| MarkTrack
    MarkTrack --> TaskLoop[Select next in-progress or pending plan task]
    TaskLoop --> NoWork{Any unfinished task remains?}
    NoWork -->|No| Finalize[Mark track completed and update metadata]
    NoWork -->|Yes| MarkTask[Mark task or sub-task in progress]
    MarkTask --> MetaTask{Is this the phase protocol meta-task?}
    MetaTask -->|Yes| PhaseProtocol[Run phase verification and checkpoint protocol]
    MetaTask -->|No| Execute[Implement smallest correct change using project conventions]
    Execute --> Verify[Run workflow-required tests, coverage, docs, and checks]
    Verify -->|Failures beyond allowed attempts| AskGuidance[Ask user for guidance]
    AskGuidance --> Execute
    Verify -->|Pass| CompleteTask[Mark task complete and record summary or commit hash]
    CompleteTask --> PhaseDone{Did this complete a phase?}
    PhaseDone -->|No| TaskLoop
    PhaseDone -->|Yes| WorkflowPhaseProtocol{Workflow defines phase completion protocol and no meta-task exists?}
    WorkflowPhaseProtocol -->|No| TaskLoop
    WorkflowPhaseProtocol -->|Yes| PhaseProtocol
    PhaseProtocol --> ModeCheck{Implementation mode?}
    ModeCheck -->|Manual| ManualSteps[Present manual verification steps]
    ManualSteps --> ManualConfirm{User confirms manual verification?}
    ManualConfirm -->|No| PhaseGuidance[Ask user for guidance and apply required fixes]
    PhaseGuidance --> PhaseProtocol
    ManualConfirm -->|Yes| CheckpointAsk{Commits authorized for this workflow?}
    CheckpointAsk -->|Yes| CheckpointCommit[Create architect checkpoint commit]
    CheckpointAsk -->|No| MarkMetaDone[Mark protocol meta-task done or record skipped checkpoint]
    ModeCheck -->|Auto| AutoVerify[Agent executes or substitutes manual verification]
    AutoVerify -->|Failures beyond allowed attempts| AskGuidance
    AutoVerify -->|Pass| CheckpointCommit
    CheckpointCommit --> RecordCheckpointHash[Record checkpoint hash in plan.md after commit]
    RecordCheckpointHash --> MarkMetaDone
    MarkMetaDone --> TaskLoop
    Finalize --> CompletionCommit{Commits authorized?}
    CompletionCommit -->|Yes| CommitComplete[Commit track completion update]
    CompletionCommit -->|No| ReportArchitectChanges[Report changed Architect files]
    CommitComplete --> DocsSync[Analyze completed track for documentation sync]
    ReportArchitectChanges --> DocsSync
    DocsSync --> DocUpdateNeeded{Product, tech stack, or guidelines update needed?}
    DocUpdateNeeded -->|No| DocsReport[Report documentation sync result]
    DocUpdateNeeded -->|Yes| DocMode{Implementation mode and document type?}
    DocMode -->|Manual or sensitive guidelines| DocApproval[Ask user to approve proposed documentation diff]
    DocMode -->|Auto routine product or tech stack docs| UpdateDocs[Apply documentation update]
    DocApproval -->|Reject| DocsReport
    DocApproval -->|Approve| UpdateDocs
    UpdateDocs --> MoreDocs{More documentation updates needed?}
    MoreDocs -->|Yes| DocMode
    MoreDocs -->|No| DocsCommit{Documentation changed and commits authorized?}
    DocsCommit -->|Yes| CommitDocs[Commit documentation sync]
    DocsCommit -->|No| DocsReport
    CommitDocs --> DocsReport
    DocsReport --> CleanupChoice[Ask user to review, archive, delete, or skip cleanup]
    CleanupChoice -->|Review| ReviewNotice[Tell user to run architect-review before cleanup]
    CleanupChoice -->|Skip| Summary[Summarize outcome]
    CleanupChoice -->|Archive| ArchiveConfirm[Ask for archive confirmation with warnings]
    CleanupChoice -->|Delete| DeleteConfirm[Ask for delete confirmation with warnings]
    ArchiveConfirm -->|Yes| Archive[Archive track safely]
    ArchiveConfirm -->|No| Summary
    DeleteConfirm -->|Yes| Delete[Delete track safely]
    DeleteConfirm -->|No| Summary
    ReviewNotice --> Summary
    Archive --> Summary
    Delete --> Summary

    class AskTrack,ModeAsk,AskGuidance,ManualSteps,ManualConfirm,CheckpointAsk,CompletionCommit,DocApproval,DocsCommit,CleanupChoice,ArchiveConfirm,DeleteConfirm human;
    classDef human fill:#fff3cd,stroke:#f0ad4e,stroke-width:2px,color:#111;
```
