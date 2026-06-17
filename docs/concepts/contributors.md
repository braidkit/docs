# Contributors

A contributor is one human or agent session acting inside a thread.

Contributors are session-shaped, not just identity-shaped. Two Codex sessions in
the same thread are two contributors. A parent agent can spawn a sub-agent by
setting `spawned_by_contributor_id`.

