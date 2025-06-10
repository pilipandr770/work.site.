#!/bin/bash

# Extract all translatable strings from the codebase
pybabel extract -F babel.cfg -k _ -k gettext -k lazy_gettext -k translate -o messages.pot .

# Update the translation files for each language
pybabel update -i messages.pot -d app/translations

echo "Translation files updated. You can now edit the .po files in app/translations/"
echo "After editing, compile the translations with: pybabel compile -d app/translations"
