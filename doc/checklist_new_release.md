The following steps should be performed when releasing a new stormpy version.

1. Update `CHANGELOG.md`
   * To get all the commits from an author since the last tag execute:
   ```console
   git log last_tag..HEAD --author "author_name"
   ```
   * Set release month

2. Update require Storm versions:
   * Update `STORM_MIN_VERSION` in `CMakeLists.txt`

3. Check that stormpy builds without errors and all tests are successful
   * [Github Actions](https://github.com/moves-rwth/stormpy/actions) should run successfully

4. Set new stormpy version:
   * Set new stormpy version in `lib/stormpy/_version.py`

5. Set new tag in git
   ```console
   git tag -a new_version
   git push github new_version
   ```
   The new tag should now be visible on [GitHub](https://github.com/moves-rwth/stormpy/tags).

6. [Add new release](https://github.com/moves-rwth/stormpy/releases/new) in GitHub.

7. Update `stable` branch:

   ```console
   git checkout stable
   git rebase master
   git push origin stable
   ```
   Note: Rebasing might fail if `stable` is ahead of `master` (e.g. because of merge commits). In this case we can do:
    ```console
   git checkout stable
   git reset --hard master
   git push --force origin stable
   ```

8. Create [Docker containers](https://hub.docker.com/r/movesrwth/stormpy) for new version using scripts.

9. Update Docker version for Binder by changing `binder/Dockerfile`:
    * Set new stormpy release as base
    * Update version numbers of dependencies

10. Create new python package for release on [Pypi](https://pypi.org/project/stormpy/):
   ```console
   python3 setup.py sdist
   python3 -m pip install --user --upgrade twine
   python3 -m twine upload dist/*
   ```

