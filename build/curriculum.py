"""The learning path for the C# / .NET book.

Chapters follow Microsoft's own ordering in `docs/csharp/toc.yml`, regrouped into a
front-to-back reading order and trimmed: reference dumps, breaking-change logs and
compiler-internals (Roslyn SDK) are left out, since they are lookup material rather
than something you read through.

Each pick is a path through the TOC by section name. `LIMIT` caps the noisier
subsections so one topic cannot swamp a chapter.
"""

# (chapter title, [(toc file, (section name path...)), ...])
CHAPTERS = [
    ("0. Setup and the .NET CLI", [
        ("files", [
            ("Introduction to .NET", "core/introduction.md"),
            ("What you can build with .NET", "core/apps.md"),
            ("Get started with .NET", "core/get-started.md"),
            ("The .NET SDK", "core/sdk.md"),
            ("Releases, patches, and support", "core/releases-and-support.md"),
            ("The dotnet command", "core/tools/dotnet.md"),
            ("dotnet new: create a project", "core/tools/dotnet-new.md"),
            ("dotnet build: compile", "core/tools/dotnet-build.md"),
            ("dotnet run: build and run", "core/tools/dotnet-run.md"),
            ("dotnet test: run tests", "core/tools/dotnet-test.md"),
            ("dotnet publish: ship it", "core/tools/dotnet-publish.md"),
            ("dotnet package add: use a library", "core/tools/dotnet-package-add.md"),
            ("dotnet format: fix style", "core/tools/dotnet-format.md"),
            ("Global, tool-path, and local tools", "core/tools/global-tools.md"),
        ]),
    ]),

    ("1. A tour of C#", [
        ("csharp", ("Get started",)),
    ]),

    ("2. Program structure and types", [
        ("csharp", ("Fundamentals", "Program structure")),
        ("csharp", ("Fundamentals", "Type system")),
    ]),

    ("3. Values, nulls, and strings", [
        ("csharp", ("Fundamentals", "Null safety")),
        ("csharp", ("Fundamentals", "Strings")),
    ]),

    ("4. Expressions, statements, and control flow", [
        ("csharp", ("Fundamentals", "Expressions and statements")),
        ("csharp", ("C# programming guide", "Statements, expressions, and equality")),
    ]),

    ("5. Object-oriented C#", [
        ("csharp", ("Fundamentals", "Object-oriented programming")),
        ("csharp", ("C# programming guide", "Classes, Structs, and Records")),
        ("csharp", ("C# programming guide", "Interfaces")),
    ]),

    ("6. Methods, delegates, and events", [
        ("csharp", ("C# concepts",)),
        ("csharp", ("C# programming guide", "Delegates")),
        ("csharp", ("C# programming guide", "Events")),
        ("csharp", ("C# programming guide", "Indexers")),
    ]),

    ("7. Generics and collections", [
        ("csharp", ("C# programming guide", "Generics")),
        ("files", [
            ("Collections and data structures", "standard/collections/index.md"),
            ("Commonly used collection types", "standard/collections/commonly-used-collection-types.md"),
            ("Selecting a collection class", "standard/collections/selecting-a-collection-class.md"),
            ("Comparisons and sorts within collections", "standard/collections/comparisons-and-sorts-within-collections.md"),
            ("Sorted collection types", "standard/collections/sorted-collection-types.md"),
            ("Hashtable and dictionary types", "standard/collections/hashtable-and-dictionary-collection-types.md"),
            ("Thread-safe collections", "standard/collections/thread-safe/index.md"),
            ("When to use a thread-safe collection", "standard/collections/thread-safe/when-to-use-a-thread-safe-collection.md"),
            ("Generic types in .NET", "standard/generics/index.md"),
            ("Generic collections in .NET", "standard/generics/collections.md"),
            ("Generic delegates for manipulating arrays and lists", "standard/generics/delegates-for-manipulating-arrays-and-lists.md"),
            ("Generic interfaces", "standard/generics/interfaces.md"),
            ("Covariance and contravariance", "standard/generics/covariance-and-contravariance.md"),
        ]),
    ]),

    ("8. LINQ", [
        ("csharp", ("Language-Integrated Query (LINQ)",)),
    ]),

    ("9. Asynchronous programming", [
        ("csharp", ("Asynchronous programming",)),
        ("files", [
            ("Async in depth", "standard/async-in-depth.md"),
            ("The task asynchronous programming model", "standard/asynchronous-programming-patterns/task-based-asynchronous-pattern-tap.md"),
            ("Consuming the task-based pattern", "standard/asynchronous-programming-patterns/consuming-the-task-based-asynchronous-pattern.md"),
            ("Parallel programming in .NET", "standard/parallel-programming/index.md"),
            ("Task parallel library (TPL)", "standard/parallel-programming/task-parallel-library-tpl.md"),
            ("Data parallelism", "standard/parallel-programming/data-parallelism-task-parallel-library.md"),
            ("Cancellation in managed threads", "standard/threading/cancellation-in-managed-threads.md"),
        ]),
    ]),

    ("10. Exceptions and functional techniques", [
        ("csharp", ("Fundamentals", "Exceptions and errors")),
        ("csharp", ("Fundamentals", "Functional techniques")),
        ("files", [
            ("Handling and throwing exceptions in .NET", "standard/exceptions/index.md"),
            ("Best practices for exceptions", "standard/exceptions/best-practices-for-exceptions.md"),
            ("Exception handling fundamentals", "standard/exceptions/exception-handling.md"),
            ("Use user-filtered exception handlers", "standard/exceptions/how-to-use-user-filtered-exception-handlers.md"),
            ("Create user-defined exceptions", "standard/exceptions/how-to-create-user-defined-exceptions.md"),
        ]),
    ]),

    ("11. Advanced C#", [
        ("csharp", ("Advanced topics", "Reflection and attributes")),
        ("csharp", ("Advanced topics", "Expression trees")),
        ("csharp", ("Advanced topics", "Performance engineering")),
        ("csharp", ("Advanced topics", "Interface implementations")),
        ("csharp", ("Advanced topics", "Native interoperability")),
    ]),

    ("12. The .NET runtime", [
        ("files", [
            ("Common Language Runtime (CLR)", "standard/clr.md"),
            ("The managed execution process", "standard/managed-execution-process.md"),
            ("Automatic memory management", "standard/automatic-memory-management.md"),
            ("Garbage collection fundamentals", "standard/garbage-collection/fundamentals.md"),
            ("Memory management and garbage collection", "standard/garbage-collection/index.md"),
            ("Workstation and server garbage collection", "standard/garbage-collection/workstation-server-gc.md"),
            ("Cleaning up unmanaged resources", "standard/garbage-collection/unmanaged.md"),
            ("Implementing a Dispose method", "standard/garbage-collection/implementing-dispose.md"),
            ("Using objects that implement IDisposable", "standard/garbage-collection/using-objects.md"),
            ("Memory and spans", "standard/memory-and-spans/index.md"),
            ("Memory-related types", "standard/memory-and-spans/memory-t-usage-guidelines.md"),
            ("Assemblies in .NET", "standard/assembly/index.md"),
            ("Reflection in .NET", "standard/attributes/index.md"),
            ("The .NET class libraries", "standard/class-libraries.md"),
            ("Framework libraries overview", "standard/runtime-libraries-overview.md"),
            ("Serialization in .NET", "standard/serialization/index.md"),
            ("JSON serialization with System.Text.Json", "standard/serialization/system-text-json/overview.md"),
            ("How to serialize and deserialize JSON", "standard/serialization/system-text-json/how-to.md"),
            ("File and stream I/O", "standard/io/index.md"),
            ("Regular expressions in .NET", "standard/base-types/regular-expressions.md"),
            ("Dates, times, and time zones", "standard/datetime/index.md"),
            ("Framework design guidelines", "standard/design-guidelines/index.md"),
            ("Naming guidelines", "standard/design-guidelines/naming-guidelines.md"),
            ("Member design guidelines", "standard/design-guidelines/member.md"),
        ]),
    ]),

    ("13. What's new in C#", [
        ("csharp", ("What's new in C#", "C# 15")),
        ("csharp", ("What's new in C#", "C# 14")),
        ("csharp", ("What's new in C#", "C# 13")),
        ("csharp", ("What's new in C#", "C# 12")),
        ("csharp", ("What's new in C#", "C# version history")),
        ("csharp", ("What's new in C#", "Relationships to .NET library")),
        ("csharp", ("What's new in C#", "Version compatibility")),
    ]),

    ("14. Guided tutorials", [
        ("csharp", ("Tutorials",)),
        ("csharp", ("Fundamentals", "Tutorials")),
    ]),
]

# Subsections that are worth reading but would otherwise dominate their chapter.
LIMIT = {
    ("csharp", ("C# programming guide", "Classes, Structs, and Records")): 18,
    ("csharp", ("Advanced topics", "Native interoperability")): 5,
    ("csharp", ("Advanced topics", "Expression trees")): 6,
    ("csharp", ("Language-Integrated Query (LINQ)",)): 20,
    ("csharp", ("Fundamentals", "Tutorials")): 8,
}

# Articles that are pure navigation stubs or duplicate a page we already include.
SKIP = {
    "csharp/how-to/index.md",
    "csharp/tour-of-csharp/tutorials/index.md",
    "csharp/programming-guide/index.md",
    "csharp/linq/how-to/index.md",
}
