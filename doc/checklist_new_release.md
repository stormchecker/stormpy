The following steps should be performed when releasing a new stormpy version.

1. Update the minimal required Storm version:
   This should be automatically handled by a CI workflow triggered by new releases in Storm.
   To manually update the Storm version:
   * change `STORM_MIN_VERSION` in `CMakeLists.txt`
   * change `STORM_GIT_TAG` in `pyproject.toml`
   Note that the CI test use the Docker `storm:ci` images which are only updated once per day.
   The CI fails if the new Storm version is not yet present in these CI Docker images.

2. Check that the stormpy [CI](https://github.com/moves-rwth/stormpy/actions/) builds without errors and all tests are successful.

3. Update `CHANGELOG.md`:
   * Set release month
   * Set major changes.
     Use the [automatically generated release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes).
     Alternatively, get all the commits since the `last_tag` by executing:
     ```console
     git log last_tag..HEAD
     ```

4. Set new stormpy version in `lib/stormpy/_version.py`

5. Create a new pull request with the changes of steps 4 and 5.
   When the CI checks are successful, stash and merge the pull request into the master branch.

6. (The tag can also automatically be set in the next step when creating the release on Github.)
   Set the new tag in Git, use the flag `-s` to sign the tag.
   ```console
   git tag -a X.Y.Z -m "Stormpy version X.Y.Z" -s
   git push origin X.Y.Z
   ```
   The new tag should now be visible on [GitHub](https://github.com/moves-rwth/stormpy/tags).

7. [Create a new release](https://github.com/moves-rwth/stormpy/releases/new) on GitHub.
   Create a new tag or use the tag created in the previous step.
   Finishing the release automatically triggers a CI workflow which also
   * updates the `stable` branch
   * creates new Docker containers for both the tag and `stable` branch
   * creates a new stormpy Python package on [Pypi](https://pypi.org/project/stormpy/)
   * triggers a PR in stormpy to update the Docker version for Binder
