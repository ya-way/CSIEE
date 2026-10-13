# Five vertical benchmark figures

User correction: restore low-scoring paper baselines; do not add a shortest-choice strategy. Restore all 12 PersonaMem configurations. Extend the same design to the other four featured benchmark families.

- Use vertical bars sorted by descending accuracy, with paper and local measurements interleaved. Preserve every row of each selected paper result column; retain a zero-based shared 0–100% scale, value labels, provenance colors and a chance line.
- Transcribe versioned primary sources: PersonaMem Figures 4/6 (12 rows), AgentSense Table 1 Info/Acc. (11), ACPBench Table 2 Mean/MCQ (22), APTBench Table 3 closed-ended Plan_EN (14), AgentHop Table 2 Outcome/Accuracy (19).
- Align aggregation: ACPBench uses equal weight across its seven MCQ tasks. APTBench uses its directly mapped 614-question English planning subtask, not the mixed-metric paper average. Label both deviations from the full-screen report card explicitly.
- Generate five PNG/SVG pairs and five combined paper/local tables from committed numerical sources. Keep the 128k PersonaMem appendix and all existing evaluation records.
- Visually inspect all figures, verify transcriptions, sorting, local counts and links, then push one commit to the existing private repository.

Verification completed: all 66 newly transcribed paper values match the primary HTML table cells; the 12 existing PersonaMem values are retained. All five figures were visually inspected. Local bars and subset counts were checked against saved predictions; all 54,344 prediction records and both original report-card tables remain consistent. README images load at desktop and mobile widths without page overflow. All 29 evaluator tests pass.
