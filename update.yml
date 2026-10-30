name: update-matches
on:
  schedule: [{cron: "*/10 * * * *"}]
  workflow_dispatch:
permissions:
  contents: write
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python update_matches.py
        env:
          FOOTBALL_DATA_TOKEN: ${{ secrets.FOOTBALL_DATA_TOKEN }}
      - run: |
          git config user.name bot && git config user.email bot@users.noreply.github.com
          git add matches.json && git commit -m "update" || exit 0
          git push
