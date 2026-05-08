$files = @("LangPacks\Main.csv", "LangPacks\Lions.csv", "LangPacks\Solo.csv", "LangPacks\Consoles.csv")

$replacements = @(
    @{ "from" = "ЗМ'ЯТІННЯ"; "to" = "СУМ'ЯТТЯ" },
    @{ "from" = "ЗМ'ЯТТЯ"; "to" = "СУМ'ЯТТЯ" },
    @{ "from" = "далекості <sprite name=Range>"; "to" = "ДАЛЬНОСТІ <sprite name=Range>" },
    @{ "from" = "Дальності <sprite name=Range>"; "to" = "ДАЛЬНОСТІ <sprite name=Range>" },
    @{ "from" = "далекості"; "to" = "дальності" },
    @{ "from" = "Вернути на руку"; "to" = "ВІДНОВИТИ" },
    @{ "from" = "Повернути на руку"; "to" = "ВІДНОВИТИ" },
    @{ "from" = "повернути на руку"; "to" = "відновити" },
    @{ "from" = "НЕВИДИМОСТЬ"; "to" = "НЕВИДИМІСТЬ" },
    @{ "from" = "Скрутою"; "to" = "Ускладненням" },
    @{ "from" = "Скрута"; "to" = "Ускладнення" },
    @{ "from" = "дальностi"; "to" = "дальності" },
    @{ "from" = "Потері"; "to" = "Втрати" },
    @{ "from" = " 03 "; "to" = " ОЗ " },
    @{ "from" = " 03,"; "to" = " ОЗ," },
    @{ "from" = " 03."; "to" = " ОЗ." },
    @{ "from" = "Рухи <sprite name=Move>"; "to" = "РУХ <sprite name=Move>" },
    @{ "from" = "розгорнути <sprite name=Refresh>"; "to" = "ОНОВИТИ <sprite name=Refresh>" },
    @{ "from" = "Розгорніть <sprite name=Refresh>"; "to" = "Оновіть <sprite name=Refresh>" },
    @{ "from" = "розгортайте <sprite name=Refresh>"; "to" = "оновлюйте <sprite name=Refresh>" }
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "Processing $file..."
        $content = Get-Content $file -Raw -Encoding UTF8
        foreach ($r in $replacements) {
            $content = $content -replace $r.from, $r.to
        }
        # Special fixes for malformed tags
        $content = $content -replace "</voffset></voffset></voffset></voffset></sprite>", "</voffset></sprite>"
        $content = $content -replace "</voffset></voffset></voffset></sprite>", "</voffset></sprite>"
        
        Set-Content $file $content -Encoding UTF8
    }
}
Write-Host "Done!"
