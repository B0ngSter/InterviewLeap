# InterviewLeap

Want to feel proud of your codebase? Following a healthy coding system is not difficult

## Frontend Nomenclature

- Class names are always singular
    - Correct: `container`, `code-block`
    - Wrong: `containers`, `code-blocks`
- In-house CSS classes are separated by underscores and contain lowercase letters only:
    - Correct: `container`, `code_block`
    - Wrong: `Container`, `codeBlock`, `CodeBlock`, `code_block`, `code-block`
- All files in the `components` directory are capitalized(first letter capital); and use CamelCase convention
    - Correct: `GoogleAuth`
    - Wrong: `google_auth`, `google-auth`, `googleAuth`
- All files in the `pages` directory:
    - Should be in lowercase letters only
    - Use hyphens instead of underscores: ex: `google-login` instead of `google_login`

### General Guidelines for a consistent codebase
- Lint your code before committing to VCS
- Best code is the one with no errors in the browser console
- Never leave any warnings un-attended in the browser console
- Always list any package dependencies in the
- Using any third-party libraries/packages should always be the last resort - try implementing small
- Follow "KISS" principle (Keep It Simple and Stupid) - write functions that do just what their name suggests
- Make your code as much "DRY (Do not Repeat Yourself)" as possible
- Use appropriate class names wherever possible - Ex: avoid using ill-logical/non-sensible variable names like `i`, `j`, `google_btn` etc.
    - In the above example, the best way to name a button for google auth is to use multiple classes, or the tag names while writing the CSS: ex: 
`button.google` or `.btn.google_auth` or `button.google_auth` etc
- While referring to any specific references online, avoid copy/paste-ing code snippets blindly - make an effort in understanding the logic and re-implement it on your own
- If you encounter writing the piece of code more than twice, consider refactoring your code to re-use the logic - `Mixins`, `Components` are a great way to achieve this; _global declarations_ are another option
- Excluding the landing pages, all the colors/fonts are to be used from the UI theme **ONLY**

## Build Setup

```bash
# install dependencies
$ npm install

# serve with hot reload at localhost:3000
$ npm run dev

# build for production and launch server
$ npm run build
$ npm run start

# generate static project
$ npm run generate
```

For detailed explanation on how things work, check out [Nuxt.js docs](https://nuxtjs.org).
