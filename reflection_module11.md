# Module 11 Reflection

## What I built

- Added a Calculation SQLAlchemy model with fields id, , , 	ype, esult.
- Created Pydantic schemas CalculationCreate and CalculationRead with validation
  (including preventing divide-by-zero when type is Divide).
- Implemented a small factory that chooses between Add, Subtract, Multiply, and Divide
  operations and used it in a create_calculation service function.
- Wrote unit tests for the factory and Pydantic validation, and an integration test that
  writes and reads Calculation rows using PostgreSQL.
- Extended the existing GitHub Actions workflow so all tests run in CI and the
  Docker image is built and pushed to Docker Hub.

## Key challenges

- **Pydantic v2 validators:** At first I tried to access alues.get("type") and hit
  a ValidationInfo error. I fixed it by switching to the Pydantic v2 style and
  reading alues.data["type"].
- **Database integration in tests:** I had to make sure the DATABASE_URL environment
  variable pointed to the Postgres container that GitHub Actions starts, and that the
  SQLAlchemy Session used the same URL.
- **Playwright in CI:** Early CI runs failed because the runner did not have the
  chromium browser installed. Adding python -m playwright install --with-deps chromium
  fixed the end-to-end test step.
- **Docker Hub permissions:** The first Docker Hub token only had read access, so
  pushes from CI failed with “access token has insufficient scopes”. I created a new
  token with Read/Write/Delete, updated the DOCKERHUB_TOKEN secret, and confirmed
  the image was pushed successfully.

## What I learned

- How to connect a FastAPI project to PostgreSQL using SQLAlchemy models.
- How to use Pydantic v2 for JSON serialization, deserialization, and validation.
- How a small factory pattern can keep calculation logic clean and easy to extend.
- How to run automated tests (unit + integration + Playwright) in GitHub Actions.
- How to build and push Docker images to Docker Hub from CI using a personal access token.
