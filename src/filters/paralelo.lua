--[[
paralelo.lua — turns the book's parallel-text tables into an Assimil-style layout.

Recognised tables (by their header row, see STYLE.md):

  |#|Pīnyīn|汉字|Español|   -> numbered dialogue, no header row
  |Pīnyīn|汉字|Español|     -> vocabulary/phrase table, header "Pīnyīn · 汉字 | Español"

In both cases the pinyin and the characters are merged into one left-hand cell
(pinyin on top, characters below in small grey type) and the Spanish goes on
the right. Italic text in the Spanish cell that starts with "(" is the literal
word-for-word translation and is set in small grey italics.
Any other table is left untouched.
]]

local is_latex = FORMAT:match("latex") ~= nil

local function raw(s)
  return pandoc.RawInline("latex", s)
end

local function inlines_of(cell)
  local out = pandoc.List()
  for _, b in ipairs(cell.contents) do
    if b.content then out:extend(b.content) end
  end
  return out
end

local function wrap(inls, latex_cmd, class)
  if is_latex then
    local out = pandoc.List({ raw("\\" .. latex_cmd .. "{") })
    out:extend(inls)
    out:insert(raw("}"))
    return out
  end
  return pandoc.List({ pandoc.Span(inls, pandoc.Attr("", { class })) })
end

local function spanish(inls)
  return pandoc.Inlines(inls):walk({
    Emph = function(e)
      local s = pandoc.utils.stringify(e)
      if s:sub(1, 1) == "(" then
        return wrap(e.content, "literal", "literal")
      end
    end,
  })
end

local function left_cell(pinyin, hanzi)
  local inls = pandoc.List()
  inls:extend(pinyin)
  if #hanzi > 0 then
    if is_latex then inls:insert(raw("\\newline ")) else inls:insert(pandoc.LineBreak()) end
    inls:extend(wrap(hanzi, "hanzi", "hanzi"))
  end
  return pandoc.Cell({ pandoc.Plain(inls) })
end

local function header_texts(tbl)
  local rows = tbl.head.rows
  if #rows ~= 1 then return nil end
  local t = {}
  for _, c in ipairs(rows[1].cells) do
    t[#t + 1] = pandoc.utils.stringify(c.contents)
  end
  return table.concat(t, "|")
end

function Table(tbl)
  local h = header_texts(tbl)
  local numbered
  if h == "#|Pīnyīn|汉字|Español" then
    numbered = true
  elseif h == "Pīnyīn|汉字|Español" then
    numbered = false
  else
    return nil
  end
  local off = numbered and 1 or 0

  for _, body in ipairs(tbl.bodies) do
    for _, row in ipairs(body.body) do
      local c = row.cells
      local cells = pandoc.List()
      if numbered then
        local n = inlines_of(c[1])
        cells:insert(pandoc.Cell({ pandoc.Plain(wrap(n, "lineno", "lineno")) }))
      end
      cells:insert(left_cell(inlines_of(c[1 + off]), inlines_of(c[2 + off])))
      cells:insert(pandoc.Cell({ pandoc.Plain(spanish(inlines_of(c[3 + off]))) }))
      row.cells = cells
    end
  end

  if numbered then
    tbl.colspecs = { { pandoc.AlignRight, 0.05 }, { pandoc.AlignLeft, 0.46 }, { pandoc.AlignLeft, 0.49 } }
    tbl.head = pandoc.TableHead({})
  else
    tbl.colspecs = { { pandoc.AlignLeft, 0.48 }, { pandoc.AlignLeft, 0.52 } }
    tbl.head = pandoc.TableHead({ pandoc.Row({
      pandoc.Cell({ pandoc.Plain({ pandoc.Str("Pīnyīn"), pandoc.Space(), pandoc.Str("·"), pandoc.Space(), pandoc.Str("汉字") }) }),
      pandoc.Cell({ pandoc.Plain({ pandoc.Str("Español") }) }),
    }) })
  end
  tbl.classes:insert(numbered and "dialogo" or "paralelo")
  return tbl
end
