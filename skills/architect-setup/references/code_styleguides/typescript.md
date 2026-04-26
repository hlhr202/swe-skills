# Google TypeScript Style Guide Summary

This document summarizes key rules and best practices from the Google TypeScript Style Guide, which is enforced by the `gts` tool.

## 1. Language Features

- **Variable Declarations:** Always use `const` or `let`. `var` is forbidden. Use `const` by default.
- **Modules:** Use ES6 modules with `import` and `export`. Do not use `namespace`.
- **Exports:** Use named exports. Avoid default exports.
- **Classes:**
  - Do not use `#private` fields. Use TypeScript's `private` visibility modifier.
  - Mark properties never reassigned outside the constructor with `readonly`.
  - Avoid the `public` modifier because it is the default.
- **Functions:** Prefer function declarations for named functions. Use arrow functions for anonymous callbacks.
- **String Literals:** Use single quotes. Use template literals for interpolation and multi-line strings.
- **Equality Checks:** Always use `===` and `!==`.
- **Type Assertions:** Avoid type assertions and non-nullability assertions. If required, provide a clear justification.

## 2. Disallowed Features

- **`any` Type:** Avoid `any`. Prefer `unknown` or a more specific type.
- **Wrapper Objects:** Do not instantiate `String`, `Boolean`, or `Number` wrapper classes.
- **Automatic Semicolon Insertion:** Do not rely on it. Explicitly end statements with semicolons.
- **`const enum`:** Do not use `const enum`. Use plain `enum` instead.
- **Dynamic Code Execution:** Do not use `eval()` or `Function(...string)`.

## 3. Naming

- **UpperCamelCase:** Classes, interfaces, types, enums, and decorators.
- **lowerCamelCase:** Variables, parameters, functions, methods, and properties.
- **CONSTANT_CASE:** Global constants and enum values.
- **Underscore Prefix/Suffix:** Do not use `_` as a prefix or suffix for identifiers, including private properties.

## 4. Type System

- **Type Inference:** Rely on inference for simple values. Be explicit for complex types.
- **`undefined` and `null`:** Both are supported. Be consistent within the project.
- **Optional Fields:** Prefer optional parameters and fields over explicit `| undefined` where appropriate.
- **Arrays:** Use `T[]` for simple types. Use `Array<T>` for complex union types.
- **Empty Object Type:** Do not use `{}`. Prefer `unknown`, `Record<string, unknown>`, or `object`.

## 5. Comments and Documentation

- **JSDoc:** Use `/** JSDoc */` for documentation and `//` for implementation comments.
- **Redundancy:** Do not declare types in `@param` or `@return` blocks when TypeScript already provides them.
- **Useful Comments:** Comments must add information, not restate the code.

Source: [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)
