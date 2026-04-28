# Word Learning App Specification

## Overview
A mobile-friendly English vocabulary learning app with multiple study modes.

## Features

### 1. Learning Modes
- **Card Flip**: Show word, tap to reveal meaning
- **Multiple Choice**: 4 options, pick correct meaning
- **Fill in Blank**: Type the spelling
- **Sentence Mode**: Learn words in context
- **Grammar Practice**: Tense, voice, clause exercises
- **Review Mode**: Spaced repetition based on due words

### 2. Word Library
- Built-in vocabularies: CET-4, CET-6, IELTS, TOEFL, Daily English
- Custom word import (JSON/TXT/CSV)
- Manual word addition

### 3. Spaced Repetition (SM-2 Algorithm)
- Track word status: new, learning, mastered
- Calculate next review date
- Ease factor adjustment

### 4. Statistics
- Daily/weekly learning count
- Accuracy rate
- Streak tracking
- Mastery distribution

### 5. Storage
- LocalStorage for all data
- No login required
- Offline available

## Tech Stack
- Single HTML file
- Pure CSS/JS
- Mobile-first responsive design
- Capacitor ready for Android APK
