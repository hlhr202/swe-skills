# Architect Review Flow

```mermaid
flowchart TD
    Start([User requests review, audit, or verification]) --> Load[Read review-protocol.md]
    Load --> Preflight[Determine whether scope is track-based or non-track]
    Preflight --> TrackBased{Track-based review?}
    TrackBased -->|Yes| SetupCheck[Verify required Architect context]
    TrackBased -->|No| WarnLimited[Warn that Architect context may be incomplete]
    SetupCheck -->|Missing required context| NotSetup[Halt and ask user to run architect-setup]
    SetupCheck -->|Ready| Parse[Parse tracks.md]
    WarnLimited --> ScopeChoice
    Parse --> ScopeChoice{Review scope supplied or inferable?}
    ScopeChoice -->|No| AskScope[Ask user to choose current changes, track, or revision range]
    ScopeChoice -->|Yes| ConfirmScope[Ask user to confirm final scope]
    AskScope --> ConfirmScope
    ConfirmScope -->|Not confirmed| AskScope
    ConfirmScope -->|Confirmed| Context[Read project context, style guides, and track context when applicable]
    Context --> Diff[Determine diff scope from track commits, current changes, or revision range]
    Diff -->|No track commits| AskDiff[Ask user how to determine review diff]
    AskDiff --> Diff
    Diff --> Volume{Diff over 300 changed lines?}
    Volume -->|Yes| LargeReview[Ask user before iterative review mode]
    Volume -->|No| Analyze[Analyze plan compliance, style, correctness, safety, tests, and docs]
    LargeReview -->|No| Summary[Summarize review cancellation]
    LargeReview -->|Yes| Analyze
    Analyze --> Report[Produce findings-first review report]
    Report --> Findings{Findings found?}
    Findings -->|No| CleanSummary[Report no findings and residual risks]
    Findings -->|Yes| NextAction[Ask how to proceed with findings]
    NextAction -->|Apply fixes| ApplyFixes[Apply approved fixes only]
    NextAction -->|Manual Fix| Summary
    NextAction -->|Complete Track| CleanupEligible{Track cleanup is eligible?}
    ApplyFixes --> ChangesMade{Did review fixes change files?}
    ChangesMade -->|No| CleanupEligible
    ChangesMade -->|Yes| TrackContext{Active track context?}
    TrackContext -->|No| CommitAsk[Ask whether to commit non-track review fixes]
    TrackContext -->|Yes| TrackRecordAsk[Ask whether to record fixes in the track plan]
    CommitAsk -->|Yes| CommitFixes[Commit review fixes]
    CommitAsk -->|No| CleanupEligible
    TrackRecordAsk -->|No| CleanupEligible
    TrackRecordAsk -->|Yes| TrackPlan[Append or reuse Review Fixes task in plan.md]
    TrackPlan --> TrackCommit{Commits authorized?}
    TrackCommit -->|Yes| CommitTrackFixes[Commit fixes and plan update]
    TrackCommit -->|No| MarkReviewTask[Mark Review Fixes task complete with no-commit]
    CommitFixes --> CleanupEligible
    CommitTrackFixes --> CleanupEligible
    MarkReviewTask --> CleanupEligible
    CleanSummary --> CleanupEligible
    CleanupEligible -->|No| Summary
    CleanupEligible -->|Yes| CleanupChoice[Offer archive, delete, or skip cleanup]
    CleanupChoice -->|Archive| ArchiveConfirm[Ask for archive confirmation with warnings]
    CleanupChoice -->|Delete| DeleteConfirm[Ask for delete confirmation with warnings]
    CleanupChoice -->|Skip| Summary
    ArchiveConfirm -->|Yes| Archive[Archive track safely]
    ArchiveConfirm -->|No| Summary
    DeleteConfirm -->|Yes| Delete[Delete track safely]
    DeleteConfirm -->|No| Summary
    Archive --> Summary
    Delete --> Summary

    class AskScope,ConfirmScope,AskDiff,LargeReview,NextAction,CommitAsk,TrackRecordAsk,TrackCommit,CleanupChoice,ArchiveConfirm,DeleteConfirm human;
    classDef human fill:#fff3cd,stroke:#f0ad4e,stroke-width:2px,color:#111;
```
