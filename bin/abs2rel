#!/usr/bin/lua

--[[
abs2rel for Lua

split and split_path taken from "Split a string with a pattern, Take Two"
  http://lua-users.org/wiki/SplitJoin
--]]

function split(str, pat)
   local t = {}  -- NOTE: use {n = 0} in Lua-5.0
   local fpat = "(.-)" .. pat
   local last_end = 1
   local s, e, cap = str:find(fpat, 1)
   while s do
      if s ~= 1 or cap ~= "" then
	 table.insert(t,cap)
      end
      last_end = e+1
      s, e, cap = str:find(fpat, last_end)
   end
   if last_end <= #str then
      cap = str:sub(last_end)
      table.insert(t, cap)
   end
   return t
end

function split_path(str)
   return split(str,'[\\/]+')
end

-- parts = split_path("/usr/local/bin")
--> {'usr','local','bin'}

function join(words, sep)
   local s = ""
   for i,v in ipairs(words) do
      s = s .. sep .. v
   end
   return string.sub (s, string.len(sep)+1)
end

function abs2rel(path, base)
   if path == base then return "." end
   local pathdirs = split_path(path)
   local basedirs = split_path(base)
   local i = 1
   local rem_i = math.min(#pathdirs, #basedirs)

   -- remove common parts of both paths
   while (rem_i > 0) and (pathdirs[i] == basedirs[i]) do
      rem_i = rem_i - 1
      table.remove(pathdirs, 1)
      table.remove(basedirs, 1)
   end

   -- now for each remaining basedirs, replace them with ..
   if #basedirs > 0 then
      for i, v in ipairs(basedirs) do
	 basedirs[i] = ".."
      end
   end
   for i, v in ipairs(pathdirs) do
      basedirs[#basedirs+1] = v
   end
   return join(basedirs, "/")
end

if #arg ~= 2 then
   io.stderr:write("usage: " .. arg[0] .. " <PATH> <BASE>\n")
   os.exit(1)
end

print(abs2rel(arg[1], arg[2]))

