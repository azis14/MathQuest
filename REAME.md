# MathQuest App

Lightweight duolingo style web application for practicing math.

## Setup
- To setup the backend. Go to the `MathQuestBE` directory and execute the [instructions](./MathQuestBE/README.md).
- To setup the frontend. Go to the `MathQuestFE` directory and execute the [instructions](./MathQuestFE/README.md).

## Time Spent (approx.)
- **Setup backend project:** ~30 min  
- **DB modeling:** ~40 min  
- **Seed script & sample content (3 lessons):** ~25 min  
- **Core features and logics + api routing and validation:** ~120 min  
- **Unit tests:** ~25 min  
- **Setup react skeleton (Vite + Tailwind), pages & API client:** ~60 min  
- **README & cleanup:** ~30 min  

**Total:** ~5h 30m

> Note: I biased toward clarity, correctness, and reviewer ergonomics over feature breadth.

## What’s Done
- **Backend:** FastAPI + async SQLAlchemy + Postgres, online Alembic migrations, seed script, layered structure (router → service → repo → models), idempotent submit via `(user_id, attempt_id)` unique constraint, daily streak logic (UTC), denormalized progress (`user_progress`), Pydantic validation, structured error shapes.
- **Frontend:** Mobile-first React app (Vite + Tailwind), lessons list, lesson play (MCQ/Input), submit flow with results modal, profile snapshot, dev proxy for easy local API.

## What I Didn’t Do (and Why)
- **Auth / sessions / multi-user signup:** out of scope; used a demo user to focus on core mechanics.
- **Comprehensive test suite & DB integration tests:** only targeted tests; full coverage would exceed the timebox.
- **Micro-interactions:** nice to have but less important than the core functional.
- **CI/CD pipeline:** local commands suffice for review.
- **Caching:** unnecessary at this scale.
- **Advanced observability:** basic logging only.

## Trade-offs & Rationale
- **Denormalized progress (`user_progress`)** to make reads cheap (lesson list/profile) while keeping writes transactional; storage overhead is tiny versus repeated computation.
- **Idempotency via DB constraint** instead of external token store: simplest, reliable, and review-friendly; can evolve to Redis tokens under heavy load.

## Approach Engaging Post-Lesson Progress Reveals Design
- **Simple popup modal:** to notify user the submission was successful and to show their progress.
- **Show the XP gained:** to motivate user for gaining more XP.
- **Show streaks:** to encourage user for keeping up with their progress.

**If have more time**
- **Add weekly leaderboards:** to motivate user do more practice.
- **Cheerful congratulate animation:** to appreciate user's effort.
- **Add next lesson suggestion:** to retain user for practicing more.

## Handling 1000+ Users Simultaneously

At this scale, the first thing we need to consider is adding advance observability tools. Before we could decide which data should be cached, which part should be optimized, etc. We need to know first the users behaviour on our system. Try to log request duration, status code, DB time per route using tools like NewRelic. It could help us pinpoint what to optimize. Beside that, it's also important to capture error on production as soon as possible. We can use Sentry to capture errors and send it to our communication tools.

After we have this data, we can start to think about how we can improve our system. Maybe we could see the most hit endpoint or the most called query first. Then we can try to add caching mechanism to that endpoint or query. Also on database level, we could try to add indexes on columns that are used frequently. For programatically approach, decoupling essential data with the additional data would help reduce response time. Only get the additional data when needed.

## Product Review (Fokuslah)

### Things That Work Well
- **Simple for practice** Easy to use the drill feature; complete with submission history.
- **Billingual content** helps people who doesn't fluent in Malay language.

### Specific Improvements
- **Add solution discussion** On the past quiz attempt, instead of only showing the correct answer, show the solution discussion.
- **Add real past math SPM file** Maybe user with pro subscription could have a list of real past math SPM file.

