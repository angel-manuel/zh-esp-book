# Build image for the Chinese-Spanish book.
# Based on the official pandoc/latex image, adding the LaTeX packages needed
# for Chinese typesetting (xeCJK) and Spanish hyphenation (polyglossia).
FROM docker.io/pandoc/latex:latest

RUN tlmgr update --self && \
    tlmgr install \
      xecjk \
      polyglossia \
      mdwtools \
      etoolbox \
      xkeyval \
      filehook \
      ucharcat \
      hyphen-spanish \
      collection-fontsrecommended && \
    tlmgr path add

# Fonts are mounted from the host at build time (see scripts/build-docker.sh),
# but we also expose a font directory inside the image so a fontconfig cache
# can pick them up.
RUN mkdir -p /usr/share/fonts/host
ENV FONTCONFIG_PATH=/etc/fonts

WORKDIR /data

# bash (the build scripts) and fontconfig (to see host-mounted fonts)
RUN apk add --no-cache bash fontconfig

# footnotehyper: footnotes inside longtable that are compatible with hyperref
RUN tlmgr install footnotehyper
