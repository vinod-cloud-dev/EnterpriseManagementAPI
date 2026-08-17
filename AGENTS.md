# Repository Guidelines

## Project Structure & Module Organization

This is a single .NET 8 ASP.NET Core Web API solution. The solution file is
`Employee_proj.sln`; application code lives in `Employee_proj/`.

- `Controllers/` contains HTTP endpoints under `/api/...`.
- `Services/` holds business logic and its interfaces; `Repository/` contains
  EF Core data-access abstractions and implementations.
- `Data/ApplicationDbContext.cs` defines the SQL Server model. EF migrations
  are in `Migrations/`.
- `Models/` contains persisted entities and `DTOs/` contains API request/read
  contracts.
- `Jobs/` contains Hangfire jobs; `Middleware/` contains cross-cutting HTTP
  middleware; uploaded product images are stored in `wwwroot/images/`.

## Build, Test, and Development Commands

Run commands from the repository root:

```powershell
dotnet restore Employee_proj.sln       # restore NuGet packages
dotnet build Employee_proj.sln         # compile the API
dotnet run --project Employee_proj     # run locally (Swagger in Development)
dotnet ef database update --project Employee_proj  # apply EF migrations
```

There is currently no test project in the solution. When one is added, run it
with `dotnet test Employee_proj.sln` and keep it in a separate `*.Tests`
project rather than inside the web project.

## Coding Style & Naming Conventions

Use C# conventions already present in the project: four-space indentation,
PascalCase for types, public members, and DTOs (`ProductCreateDto`), camelCase
for parameters and locals, and interface names prefixed with `I`
(`IProductService`). Keep controller actions thin; place business rules in
services and SQL/EF queries in repositories. Prefer async EF APIs and append
`Async` to asynchronous method names. No formatter or linter is currently
configured, so format code consistently with nearby files and build before
submitting.

## Configuration, Security, and Jobs

Use `appsettings*.json` only for non-secret local defaults. Do not commit JWT
keys, SMTP passwords, or production connection strings; use user secrets or
environment variables. Product categories use Redis caching, while product
reads use in-process memory caching—preserve cache invalidation when changing
write operations. Hangfire uses SQL Server storage; make jobs idempotent and
safe to retry.

## Commit & Pull Request Guidelines

Recent history uses short, imperative descriptions such as `Added Hangfire for
Backgroud Jobs`; use clearer equivalents, e.g. `Add product cache invalidation`.
Keep commits focused. Pull requests should explain the API/behavior change,
list configuration or migration steps, link the relevant issue when available,
and include Swagger screenshots or sample requests for endpoint changes.
