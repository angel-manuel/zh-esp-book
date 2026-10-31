# Chino mandarín para hispanohablantes

Curso de chino mandarín (caracteres simplificados) para hispanohablantes, al estilo
**Assimil**: lecciones cortas con el texto en **pinyin** a la izquierda (con los caracteres
debajo en gris, para cuando des el salto) y el **español** a la derecha, con traducción
literal cuando ayuda. Entre las lecciones hay capítulos de **teoría** (pinyin, tonos,
clasificadores, aspecto…) y de **cultura**.

El objetivo no es sólo hablar: es poder mantener **conversaciones importantes con
personas chinas** (negocios, banquetes, relaciones a largo plazo, temas delicados)
transmitiendo respeto y comprensión de su visión del mundo.

Hermano de `ruso-esp-book` y `jpn-esp-book` (mismo flujo: Markdown → Pandoc → XeLaTeX).

## Método

- **Fase pasiva (lecciones 1-49):** escucha, lee el pinyin, compara con el español, repite
  en voz alta. Media hora al día. Sin memorizar a la fuerza.
- **Segunda ola (desde la lección 50):** cada día, además de la lección nueva, retomas una
  antigua y la traduces del español al chino. Ahí lo pasivo se vuelve activo.
- Cada 7.ª lección es un **repaso**. Los capítulos de teoría y cultura se leen cuando
  aparecen en el orden del libro.

Currículo completo y mapa de archivos: [CURRICULUM.md](CURRICULUM.md)
(91 lecciones, 11 de teoría, 8 de cultura, apéndices).

## Estructura

```
zh-esp-book/
├── src/chapters/        # NNN-tipo-NN-slug.md (el prefijo de 3 cifras decide el orden)
├── src/filters/         # paralelo.lua: maqueta las tablas Pīnyīn|汉字|Español estilo Assimil
├── src/templates/       # bilingual.tex (PDF) y style.css (HTML)
├── src/metadata.yaml
├── scripts/
│   ├── build.sh         # build.sh [pdf|html] [glob]   p. ej. build.sh pdf 004
│   ├── build-docker.sh  # lo mismo dentro de un contenedor con xeCJK
│   ├── lint.py          # formato (tablas, pinyin con tonos, notas…)
│   └── check-pinyin.sh  # contrasta el pinyin con los caracteres (pypinyin, vía uv)
├── audio/               # MP3 por archivo (generados, no versionados)
├── STYLE.md             # guía de estilo: obligatoria para escribir
└── CURRICULUM.md
```

## Compilar

```bash
scripts/build.sh               # libro completo → output/chino-espanol.pdf
scripts/build.sh pdf 004       # sólo la lección 1 → output/test.pdf
scripts/build.sh html          # versión HTML
scripts/lint.py && scripts/check-pinyin.sh --tones
```

`build.sh` usa XeLaTeX con xeCJK; si no los tienes instalados, compila automáticamente
dentro de un contenedor (docker o podman), que se construye la primera vez.

## Licencia

MIT
