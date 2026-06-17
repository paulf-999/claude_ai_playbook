# No tool agent for data_pipeline style guide
**Date:** 2026-06-09
**Status:** active

No dedicated tools agent was created for `data_pipeline.md`, despite the convention of "one agent per style guide".

**Rationale:** Tool agents are useful because they own specific file patterns — the dbt agent reviews `models/**/*.sql`, the airflow agent reviews `dags/**/*.py`. `data_pipeline.md` is a cross-cutting patterns guide with no file type to own. An agent with no file ownership and no distinct scope from the existing `architect` agent would add noise without value. The `architect` agent is the natural agent for pipeline design reviews and already applies these principles.
