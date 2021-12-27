### Installation (one time)
Use `./install_git_hooks.sh` to install _pre-commit_ and _pre-push_ git hooks.

### Working
Codes in _pre-commit_ and _pre-push_ must pass for commit and push to succeed respectively.

### Covered design principles
#### Pre-commit
1. Linting (`pylint`)
2. Cyclomatic complexity (`radon cc`) *_(Single Responsibility Principle - SRP)_*

#### Pre-push
1. Unittests (`nose2`)
2. Coverage (`nose2 -C`)

### Future Scope
1. Flake8 (and/or `pylint`)
2. Manegability Index (`radon mi`)
3. Raw metrics (`randon raw`)
4. Halstead complexity metrics (`radon hal`)
5. Cross-modules Copy Paste Detector (CPD) *_(Do not Repeat Yourself - DRY principle)_*
6. `nose2-spark` (Tests for spark modules)
7. [Other libraries for analysis](https://github.com/mre/awesome-static-analysis#python)
