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
`.github/workflows/build-apk.yml` builds the debug APK on every push to `main` and every pull request.
Download it from the run's **Artifacts** section on the Actions tab. You can also start a build by hand
from the Actions tab (**Build APK → Run workflow**).

To publish a release, push a version tag. The APK is attached to a new GitHub Release:

    git tag v1.3
    git push origin v1.3

## Play Store release
Create an upload keystore (keep it safe; you need it for every future update), then build a signed bundle:

    keytool -genkey -v -keystore letterlock-upload.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload
    cd android && ./gradlew bundleRelease

and sign it in Android Studio (Build > Generate Signed Bundle) or via `signingConfigs` in `android/app/build.gradle`.
Bump `versionCode` / `versionName` in `android/app/build.gradle` for each release.
