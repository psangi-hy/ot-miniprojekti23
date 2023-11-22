# Elastinen

![GHA workflow badge](https://github.com/psangi-hy/ot-miniprojekti23/workflows/CI/badge.svg)


 [Backlog (Google Docs)](https://docs.google.com/spreadsheets/d/17COsn4LBcv9tK5OwG2H8qlhSb43Yw5VLccIJSeliQN4/edit#gid=0)

## Definition of Done
* Product backlogin jokaisella sprinttiin valitulla user storylla on kirjattu hyväksymiskriteerit
* Koodilla on kohtuullinen testikattavuus
* Asiakas pääsee näkemään koko ajan koodin ja testien tilanteen CI-palvelusta
* Koodin ylläpidettävyys on hyvä
    * selkeä arkkitehtuuri, koodin eri toiminnallisuudet ovat omissa tiedostoissaan
    * järkevä nimeäminen
    * yhtenäinen koodityyli (noudattaa pylintin avulla määriteltyjä sääntöjä)

## Sovelluksen asennus- ja käyttöohje
**Huom:**
Asentamisen ohjeet ovat hieman erilaisia riippuen käyttöjärjestelmästä (Linux/Windows/Mac). Seuraavat esimerkkiohjeet ovat Linuxille. Oletus on että käytössäsi on Python3, poetry  ja [SQLite](https://www.sqlite.org/download.html).

1. Lataa sovelluksen GitHub-repository yhteen kansioon

2. Riippuvuuksien injektointi terminaalissa
```bash
poetry install
```

3. Käynnistä virtuaaliympäristö terminaalissa
```bash
poetry shell
```

4. Käynnistä sovellus
```bash
flask run
```
