# Letterlock

A word-guessing game (Gauntlet, Daily Word, Lightning, Showdown, Practice) that runs on the web and as an Android app via Capacitor.

## Features
- Modes: Gauntlet, Daily Word, Lightning, Showdown (vs computer or pass and play), Practice
- Showdown uses game-show rules: control passes on an invalid word or timeout (with a bonus letter), a steal row after 5 misses,
  ball draws onto a 5×5 lock card after each solve (lines +100, gold and red balls), sudden death on a tie, and a Jackpot round for the winner
- Computer opponent with Easy / Normal / Hard skill (roughly 47% / 85% / 99% of words solved within 5 rows)
- Gauntlet gives a bonus letter and one last-chance guess before you lose a life
- Daily Word progress is saved after every guess
- Hints: Clue (definition, then example sentence), Reveal, Sweep, Freeze
- Coins and XP from every solve, ranks from Rookie to Lexicon Legend
- Three daily missions, a 7-day login bonus, golden words worth double
- Word book of every solved word with its meaning; 4 themes to unlock; 25 awards

## Layout
- `index.html`, `words.json`: the game (the web version is published from these directly)
- `assets/fonts/`: bundled fonts so the app works offline
- `scripts/build-www.sh`: builds the offline app bundle in `www/`
- `scripts/build-words.py`, `scripts/build-defs.py`: rebuild the dictionary and the clue definitions (WordNet)
- `scripts/make-icons.js`: renders launcher icons and splash screens (needs Playwright)
- `capacitor.config.json`, `android/`: the Capacitor Android project

## Build the APK
Needs Node 20+, JDK 21 and the Android SDK (platform 36). Put `sdk.dir=/path/to/android-sdk` in `android/local.properties`.

    npm install
    npm run apk

The debug APK lands in `android/app/build/outputs/apk/debug/app-debug.apk`.
Or open the project in Android Studio with `npx cap open android`.

### On GitHub
`.github/workflows/build-apk.yml` builds the app on every push to `main` and every pull request; you can also
start it from the Actions tab (**Build APK → Run workflow**). Download the result from the run's **Artifacts** section.
Once the signing secrets below are set, each run produces a signed `Letterlock-<version>.apk` and a
`Letterlock-<version>.aab` for the Play Store. Without them it falls back to a debug APK.

To publish a release, push a version tag. The files are attached to a new GitHub Release:

    git tag v1.3
    git push origin v1.3

Remember to raise `versionCode` and `versionName` in `android/app/build.gradle` before each release.

## Release signing
Every release must be signed with the same key, or Android refuses to install it over the previous version.
Create the key once, on your own computer (needs a JDK for `keytool`):

    bash scripts/make-signing-key.sh

The script writes the key to `~/letterlock-signing/` and prints the 4 secrets to add under
**Settings → Secrets and variables → Actions**: `ANDROID_KEYSTORE_BASE64`, `ANDROID_KEYSTORE_PASSWORD`,
`ANDROID_KEY_ALIAS` and `ANDROID_KEY_PASSWORD`. It also writes `android/keystore.properties` (git-ignored),
so `npm run apk:release` signs local builds with the same key.

Back up `~/letterlock-signing/` somewhere private. Never commit the key. If you publish on Google Play with
Play App Signing, this key is your *upload key*, and Google can reset it if it's lost.

## Play Store release
1. Set up release signing (above) and raise `versionCode` / `versionName` in `android/app/build.gradle`.
2. Push a version tag, or run the workflow by hand, and download `Letterlock-<version>.aab`.
3. Upload the `.aab` in the Google Play Console. Opt in to Play App Signing when asked.
