# Guía de estilo y formato — Chino mandarín para hispanohablantes

Referencia obligatoria para escribir cualquier archivo de `src/chapters/`. El libro se
compila con Pandoc + un filtro Lua (`src/filters/paralelo.lua`) + XeLaTeX: una tabla mal
formada rompe la maqueta. Después de escribir, ejecuta `scripts/lint.py` y
`scripts/check-pinyin.sh` y corrige todo lo que señalen.

## 1. Público, objetivo y tono

- **Lector:** hispanohablante adulto, cero conocimientos previos. Quiere hablar y entender
  mandarín **leyendo pinyin** primero; los caracteres llegan después, de forma gradual.
- **Objetivo final:** poder mantener conversaciones importantes (negocios, banquetes,
  relaciones a largo plazo, temas delicados) **transmitiendo respeto y comprensión** de la
  visión china del mundo. La cultura no es un adorno: es la mitad del libro.
- **Prosa en español neutro**, directa, sin regionalismos. Trata al lector de **tú**.
- **Chino:** mandarín estándar de la China continental (普通话), **caracteres simplificados**.
  Natural y correcto: frases que diría un chino real, no traducciones palabra por palabra.
  Registro por defecto: cortés-neutro; formal (您, 请, 贵公司…) en las escenas de negocios.
- **Cultura con respeto, sin propaganda ni caricatura.** Explica cómo ven las cosas los
  chinos y por qué, describe las diferencias con España sin juzgar, y da consejos
  prácticos. En temas políticos, presenta la perspectiva china mayoritaria con honestidad,
  señala que existen otras, y céntrate en cómo comportarse. Nunca estereotipos.

### Personajes recurrentes

| Personaje | Pīnyīn | 汉字 | Papel |
|:--|:--|:--|:--|
| Carlos | Kǎluòsī | 卡洛斯 | español de Madrid, ingeniero; viaja a China por trabajo (protagonista) |
| Lucía | Lùxīyà | 露西亚 | su compañera de empresa, estudia chino con él |
| Wáng Fāng | Wáng Fāng | 王芳 | amiga de Pekín, profesora de español; les explica la cultura |
| Lǐ Míng | Lǐ Míng | 李明 | contacto de negocios en Shanghái, de la edad de Carlos |
| Zhāng zǒng | Zhāng zǒng | 张总 | director general de la empresa de Lǐ Míng (el alto cargo) |
| Chén lǎoshī | Chén lǎoshī | 陈老师 | profesora de chino de Carlos (en las lecciones de teoría) |

Más personal según la escena: 服务员 fúwùyuán (camarero), 司机 sījī (conductor),
师傅 shīfu (tratamiento para taxistas, técnicos…), 前台 qiántái (recepción), 医生 yīshēng.

## 2. El pinyin (reglas estrictas)

1. **Siempre con marcas de tono**: nǐ hǎo, xièxie, Zhōngguó. Nunca números (ni3) ni pinyin
   sin tono. ü se escribe ü (nǚ, lǜ); tras j/q/x/y se escribe u (qù, xué, yú).
2. **Tono neutro sin marca**: xièxie, māma, de, le, ma, ne, ba, men, zi (yǐzi), shēngri…
3. **Cambios de tono (sandhi):**
   - 不 y 一 se escriben **con el tono que realmente se pronuncia**: bú shì, bú yào,
     yí gè, yì tiān, yìqǐ; y su tono original en citas aisladas y al final (yī, dì-yī).
   - El 3.º+3.º tono se escribe **con su tono original** (nǐ hǎo, no ní hǎo). Se explica en
     la teoría y se recuerda en notas, pero no se marca.
4. **Ortografía por palabras** (norma GB/T 16159): las sílabas de una palabra van juntas
   (Zhōngguó, péngyou, xǐhuan, gōngsī), las palabras separadas por espacios
   (Wǒ shì Xībānyá rén.). Clasificador separado (yí gè rén). 的/了/吗/呢 separados.
5. **Apóstrofo** ante sílaba que empieza por a, o, e dentro de una palabra: Xī'ān, Tiān'ānmén, nǚ'ér.
6. **Mayúscula** al inicio de frase y en nombres propios: Běijīng, Wáng Fāng (apellido y
   nombre separados, ambos con mayúscula), Zhāng zǒng, Chén lǎoshī.
7. **Puntuación occidental** en el pinyin (`.`, `,`, `?`, `!`, `"…"`), **sin** ¿ ¡ (eso es
   para el español). En la columna 汉字, puntuación china de anchura completa: `，。？！、「」` o `“”`.
8. Erhua (儿): úsalo con moderación, en palabras muy comunes (yìdiǎnr 一点儿, nǎr 哪儿).
   Indica en una nota que en el sur se dice yìdiǎn, nǎlǐ.

## 3. Tablas: el corazón del libro

El filtro Lua reconoce **dos cabeceras exactas** y las maqueta en estilo Assimil: a la
izquierda el pinyin con los caracteres debajo en gris pequeño, a la derecha el español.
Cualquier otra tabla se deja tal cual (tablas de gramática, comparaciones, etc.).

### 3.1 Diálogo numerado (texto de cada lección)

```markdown
|#|Pīnyīn|汉字|Español|
|:-|:-----|:---|:------|
|1|Kǎluòsī: Nǐ hǎo! Wǒ jiào Kǎluòsī.|卡洛斯：你好！我叫卡洛斯。|Carlos: ¡Hola! Me llamo Carlos. *(tú bien / yo llamarse Carlos)*|
|2|Wáng Fāng: Nǐ hǎo! Wǒ xìng Wáng, jiào Wáng Fāng.|王芳：你好！我姓王，叫王芳。|Wang Fang: ¡Hola! Me apellido Wang, me llamo Wang Fang.|
```

### 3.2 Vocabulario y frases

```markdown
|Pīnyīn|汉字|Español|
|:-----|:---|:------|
|péngyou|朋友|amigo, amiga|
|Wǒ shì Xībānyá rén.|我是西班牙人。|Soy español(a). *(yo ser España persona)*|
```

Reglas:

1. Cabecera y orden exactos: `#|Pīnyīn|汉字|Español` o `Pīnyīn|汉字|Español` (con los
   macrones de Pīnyīn). El separador puede ser cualquier `|:-|`.
2. **Traducción literal**: tras la traducción natural, entre paréntesis y en cursiva,
   `*(yo ser España persona)*`, cuando aporte algo (orden de palabras, estructura nueva).
   No en cada línea: en 3-5 líneas por diálogo, menos a medida que avanza el libro.
   Debe empezar por `(` dentro de los asteriscos para que el filtro la ponga en gris.
3. Hablante al inicio de las tres columnas: pinyin `Kǎluòsī:`, 汉字 `卡洛斯：`, español
   `Carlos:`. En español los nombres chinos van **sin tonos**: Wang Fang, Li Ming,
   el director Zhang, la profesora Chen.
4. Una fila = una línea. Nada de `<br>`, HTML, LaTeX ni `|` dentro de una celda.
5. **Una línea en blanco antes y después** de cada tabla.
6. Llamadas a nota dentro de una celda: sólo en la columna Español o Pīnyīn, ver §6.

## 4. Tipos de archivo y estructura

Todo archivo empieza con este frontmatter; el H1 repite el `title` exactamente:

```markdown
---
title: "Lección 1 · ¡Hola! (Nǐ hǎo!)"
---

# Lección 1 · ¡Hola! (Nǐ hǎo!)
```

Formatos de título: `Lección N · Título (Pīnyīn)`, `Teoría N · Título`,
`Cultura N · Título`, `Apéndice N · Título`. Los encabezados H2/H3 van en español; puedes
añadir el término chino entre paréntesis: `## Notas (zhùshì 注释)`.

### 4.1 Lección (L) — corta, estilo Assimil (120-220 líneas)

```markdown
## Texto (kèwén 课文)
(una o dos frases en español que sitúan la escena)
(diálogo numerado, 8-14 líneas; repasos: 12-18)

## Palabras nuevas
(tabla Pīnyīn|汉字|Español con las 10-25 palabras nuevas de la lección)

## Notas
**(1)** Explicación breve ligada a la línea 1 del texto…
**(3)** …
(4-8 notas; cada una 2-6 frases, con mini-tablas de ejemplos si hace falta)

## Ejercicio 1 · Traduce
(5 frases en pinyin con caracteres, el lector traduce al español)

## Ejercicio 2 · Completa
(4-5 frases en pinyin con huecos ___ y su traducción española)

## Soluciones
(soluciones de ambos ejercicios en la misma lección, como en Assimil)

## Cultura (wénhuà 文化)        ← opcional, 1-2 párrafos
## Segunda ola                   ← sólo desde la lección 50: «Retoma la lección N−49…»
```

- **Gramática a dosis pequeñas**, en las notas. Cada lección introduce 1-2 puntos nuevos
  y 15-25 palabras nuevas, y recicla lo anterior. Usa sólo vocabulario ya visto o
  presentado en la propia lección.
- Las primeras lecciones (1-14) llevan **consejos de pronunciación** en las notas (tonos,
  sílabas difíciles para hispanohablantes: zh/ch/sh/r, j/q/x, ü, -n/-ng, aspiradas).
- Indica el audio al principio del texto: `> Audio: audio/NNN.mp3` (el número del archivo).

### 4.2 Lección de repaso (cada 7.ª)

- `## Repaso de gramática`: resumen numerado de lo visto en las 6 lecciones anteriores,
  con remisiones («ver lección 3, nota 2»).
- `## Texto de repaso`: diálogo más largo que sólo usa lo ya visto.
- `## Ejercicio`, `## Soluciones`. Sin vocabulario nuevo (o casi).

### 4.3 Teoría (T) — explicativa (250-450 líneas)

Explica un sistema completo (los tonos, los clasificadores, el aspecto…) con tablas,
muchos ejemplos en tablas paralelas, errores típicos de hispanohablantes, 3-4 ejercicios y
`## Soluciones` al final. Personaje: Chén lǎoshī puede aparecer en un diálogo ilustrativo.

### 4.4 Cultura (C) — capítulos de fondo (300-550 líneas)

Prosa en español, con estructura clara: el concepto, por qué es así (historia,
filosofía), cómo se manifiesta, **qué hacer y qué evitar** (tabla o lista), errores
típicos de occidentales, y **frases útiles** en una tabla `Pīnyīn|汉字|Español`. Incluye
al menos un **diálogo de ejemplo** comentado (bien hecho / mal hecho). Cierra con
`## Puntos clave` (5-8 viñetas). Sin ejercicios obligatorios.

## 5. Contenido cultural: cobertura y enfoque

Temas que el libro debe tratar a lo largo de las lecciones y capítulos de cultura:

- 面子 miànzi (la cara), 关系 guānxi, 人情 rénqíng (deuda de favores), jerarquía y edad,
  armonía (和), modestia (谦虚), lo colectivo frente a lo individual.
- La mesa: banquetes, asientos, anfitrión, brindis por rango, 白酒, rechazar bebida sin
  ofender, pelear la cuenta, té, KTV.
- Regalos, 红包, números y colores, tabúes.
- Negocios: tarjetas, títulos, reuniones, negociación indirecta, el «sí» que no es sí,
  contratos y relación, intermediarios, intérpretes, WeChat como herramienta de trabajo.
- Visión del mundo: continuidad histórica, el «siglo de humillación», confucianismo,
  estabilidad, desarrollo, orgullo nacional; temas delicados y cómo manejarlos.

Enfoque: **comprender antes que opinar**. Cuando un tema es delicado, explica qué siente
el interlocutor, qué frases evitar, y cómo responder si te preguntan (con fórmulas en
chino). Nunca pongas en boca de los personajes chinos caricaturas ni discursos oficiales
largos; deben ser personas normales, amables, con opiniones matizadas.

## 6. Notas al pie

- Úsalas poco (en lecciones, las notas numeradas sustituyen a las notas al pie).
- Identificador con el prefijo del archivo: `[^c052-mianzi]` en `052-…md`; único en el libro.
- La definición va **después de la tabla, tras una línea en blanco**, nunca dentro.

## 7. Frases pedidas por el autor

Estas frases deben aparecer pronto y con notas sobre su uso real (ya distribuidas):
你好吗 / 最近怎么样 y 吃饭了吗 / 吃好了吗 (lección 1); 你懂吗 / 你明白吗 /
我说清楚了吗 y 我不知道 (lección 2); 都行 / 都可以 / 随便 / 无所谓, con sus matices
(lección 3). Recíclalas en lecciones posteriores.

## 8. Otras reglas de formato

- Usa la raya `—` en la prosa y `…` (un carácter). Para patrones gramaticales escribe
  `太…了`, `tài … le`. Nunca `~` ASCII (Pandoc lo convierte en subíndice).
- Sin HTML ni LaTeX en los capítulos.
- Las listas y tablas de gramática que no son paralelas pueden tener cualquier
  número de columnas, siempre con cabecera.
- Cifras en español con coma decimal y punto de miles; en chino, números arábigos o
  caracteres según lo natural (3 块, 三个人).
