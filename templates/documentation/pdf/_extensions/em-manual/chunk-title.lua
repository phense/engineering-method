-- Quarto book composition inserts a title header and a quarto-title-block
-- before the original chapter body. Our chunk contract already has a matching
-- H1. Remove only that generated header before cross-reference numbering;
-- retain the metadata block and authored heading, including its stable ID.
return {{
  Blocks = function(blocks)
    local result = pandoc.List()
    local i = 1
    while i <= #blocks do
      local first, metadata, authored = blocks[i], blocks[i + 1], blocks[i + 2]
      if authored and first.t == "Header" and first.level == 1
          and metadata.t == "CodeBlock" and metadata.classes:includes("quarto-title-block")
          and authored.t == "Header" and authored.level == 1
          and pandoc.utils.stringify(first.content) == pandoc.utils.stringify(authored.content) then
        result:insert(metadata)
        result:insert(authored)
        i = i + 3
      else
        result:insert(first)
        i = i + 1
      end
    end
    return result
  end,
}}
