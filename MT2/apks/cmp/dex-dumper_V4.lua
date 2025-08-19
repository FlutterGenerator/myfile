gg.alert("GO to Settings At the top of the list from gameguardian And choose hide gameguardian from the game and set 1 2 3 to true")

gg.alert("What's New: Dexprotector dumper Added \n\n\n Head 037 has been added.  \nYou should know that most applications use header 035, so if you fail at 035, try again at 037.\n\nImportant Note: you have to Select the memory that have dexs in order for it to be found For Example J(java)")

        local dumpDex = {}

function dumpDex:getTargetPackage()
	return gg.getTargetPackage()
end

function dumpDex:getPackageName()
	return self.targetPackage
end

function dumpDex:setPackageName(targetPackage)
	self.targetPackage = targetPackage
end

function dumpDex:getRootDir()
	return string.format('%s/dumpDex', gg.EXT_STORAGE)
end

function dumpDex:getDumpDir()
	return string.format('%s/%s', self:getRootDir(), self:getPackageName())
end

function dumpDex:getRangeMap()
	local rangeMap = self.rangeMap
	if rangeMap then
		return rangeMap
	end

	rangeMap = {
		Jh = gg.REGION_JAVA_HEAP,
		Ch = gg.REGION_C_HEAP,
		Ca = gg.REGION_C_ALLOC,
		Cd = gg.REGION_C_DATA,
		Cb = gg.REGION_C_BSS,
		PS = gg.REGION_PPSSPP,
		A = gg.REGION_ANONYMOUS,
		J = gg.REGION_JAVA,
		S = gg.REGION_STACK,
		As = gg.REGION_ASHMEM,
		V = gg.REGION_VIDEO,
		O = gg.REGION_OTHER,
		B = gg.REGION_BAD,
		Xa = gg.REGION_CODE_APP,
		Xs = gg.REGION_CODE_SYS
	}
	self.rangeMap = rangeMap
	return rangeMap
end

function dumpDex:getRangeText()
	local rangeMap = self:getRangeMap()
	local rangeValue = gg.getRanges()
	local ranges = {}

	for k, v in pairs(rangeMap) do
		if (rangeValue & v) == v then
			ranges[#ranges + 1] = k
			rangeValue = rangeValue & ~v
		end
	end

	return table.concat(ranges, ' | ')
end

function dumpDex:getRangeNames()
	local map = self:getRangeMap()
	local list = {}
	for k, v in pairs(map) do
		list[#list + 1] = k
	end
	return list
end

function dumpDex:selectRange()
	local names = self:getRangeNames()
	local selection = {}
	local rangeMsg = self:getRangeText()

	local curRangName = {}
	for name in string.gmatch(rangeMsg, '%w+') do
		curRangName[name] = true
	end

	for i, name in ipairs(names) do
		selection[i] = (curRangName[name] == true)
	end

	local inputs = gg.multiChoice(names, selection, string.format('Current selection：%s', rangeMsg))
	if not inputs then
		return
	end

	local map = self:getRangeMap()
	local rangeValue = 0
	for i, v in pairs(inputs) do
		if v then
			local name = names[i]
			rangeValue = rangeValue | map[name]
		end
	end

	gg.setRanges(rangeValue)
end

function dumpDex:newDex(address)
	local dex = {}
	setmetatable(dex, {
		__index = self
	})

	function dex:getAddress()
		return address
	end

	function dex:getName()
		local dexName
		local index = self.index
		if type(index) ~= 'number' then
			error('need dex.index = number', 2)
		end
		if index == 1 then
			dexName = 'classes.dex'
		else
			dexName = string.format('classes%d.dex', index)
		end
		return dexName
	end

	function dex:getRangesInfo()
		local rangesInfo = self.rangesInfo
		if rangesInfo then
			return rangesInfo
		end

		local address = self:getAddress()
		local rangesInfo
		local RangesList = gg.getRangesList()
		for _, info in ipairs(RangesList) do
			local startAddr = info.start 
			local endAddr = info['end']

			-- Find the information about dex in memory
			if startAddr <= address and address <= endAddr then


				if not rangesInfo or rangesInfo['end'] < info['end'] then
					rangesInfo = info
				end
			end
		end

		if not rangesInfo then
			error(string.format('%s could not find it rangesInfo', self:getName()), 2)
		end

		self.rangesInfo = rangesInfo
		return rangesInfo
	end

	function dex:getStartAddr()
		return self:getRangesInfo().start
	end

	function dex:getEndAddr()
		return self:getRangesInfo()['end']
	end

	function dex:getDexPosition()
		return self:getAddress() - self:getStartAddr()
	end

	function dex:assertProcess()
		local targetPackage = self:getTargetPackage()
		local packageName = self:getPackageName()

		if targetPackage ~= packageName then
			error(string.format('The process has changed %s>%s', packageName, targetPackage), 2)
		end
	end

	function dex:getDumpMemoryPath(startAddr, endAddr, dumpDir, packageName)
		if not packageName then
			packageName = gg.getTargetPackage()
		end
		return string.format('%s/%s-%x-%x.bin', dumpDir, packageName, startAddr, endAddr)
	end

	function dex:dumpMemory(startAddr, endAddr, dumpDir)
		local res = gg.dumpMemory(startAddr, endAddr - 1, dumpDir)
		if res ~= true then
			return false, res
		end

		return self:getDumpMemoryPath(startAddr, endAddr, dumpDir, self:getPackageName())
	end

	function dex:dump()
		self:assertProcess()

		local startAddr = self:getStartAddr()
		local endAddr = self:getEndAddr()
		local dumpDir = self:getDumpDir()

		local path, err = self:dumpMemory(startAddr, endAddr, dumpDir)
		if not path then
			error(string.format('Unable to export memory\n%s', err), 2)
		end

		return path
	end

	function dex:getSize()
		local dexSize = self.dexSize
		if dexSize then
			return dexSize
		end

		local offset = 32
		local value = {
			address = self:getAddress() + offset,
			flags = gg.TYPE_DWORD
		}
		local vlaues = {value}
		vlaues = gg.getValues(vlaues)
		dexSize = vlaues[1].value

		self.dexSize = dexSize
		return dexSize
	end

	function dex:getDexOutPath()
		return string.format('%s/%s', self:getDumpDir(), self:getName())
	end

	function dex:getDexOutFile(path)
		return assert(io.open(path, 'w'))
	end

	function dex:getDexInputFile(path)
		local f = assert(io.open(path, 'r'))
		f:seek('cur', self:getDexPosition())
		return f
	end

	function dex:checkSize()
		-- Normally, the DEX size should be a positive number and smaller than the maximum range of memory.
		return dex:getSize() > 0 and dex:getSize() < (dex:getEndAddr() - dex:getStartAddr())
	end

	function dex:out(outPath)
		local binPath = self:dump()
		local inputf = self:getDexInputFile(binPath)
		local dexSize = self:getSize()
		local readSize = 1024 * 1024 * 1
		if dexSize < readSize then
			readSize = dexSize
		end

		if not outPath then
			outPath = self:getDexOutPath()
		end
		local outf = self:getDexOutFile(outPath)

		local readLength = 0

		-- Extract DEX from the bin file exported from memory
		local function copy()
			while true do
				local tmp = inputf:read(readSize)
				outf:write(tmp)
				readLength = readLength + readSize

				if readLength >= dexSize then
					inputf:close()
					outf:close()
					break
				end
			end
		end

		local ok, err = pcall(copy)

		-- Delete exported memory files
		os.remove(binPath)

		if not ok then
			-- An error occurred while copying DEX. Delete the error file.
			os.remove(outPath)
			return false, err
		end

		-- Returns the exported DEX file path
		return outPath
	end

	return dex
end

function dumpDex:results2dexs(results)
	local dexs = {}

	for i = 1, #results do
		local value = results[i]
		local address = value.address
		local dex = self:newDex(address)

		if dex and dex:checkSize() then
			local index = #dexs + 1
			dex.index = index
			dexs[index] = dex
		end
	end

	return dexs
end


function dumpDex:results2dexs2(results)
	local dexs = {}
	for i = 1, #results do
		local value = results[i]
		local address = value.address
		local dex = self:newDex(address)

		if dex and dex:checkSize() then
			local index = #dexs + 1
			dex.index = index
			dexs[index] = dex
		end
	end

	return dexs
end

function dumpDex:getDexs()

	  gg.clearResults()   
       
      local classes = {}
      classes['dexs'] = {}
      classes['Check'] = {}
      classes['Verified'] = {}
      Search = 1
      
      gg.searchNumber(3486512, 4) 
      
      local Results1 = gg.getResults(250)
      
    for index, value in ipairs(Results1) do   
    classes['dexs'][Search] = {}
    classes['dexs'][Search].address = Results1[index].address + -4
	classes['dexs'][Search].flags = 4
	classes['Check'][Search] = {}
	classes['Check'][Search].address = Results1[index].address + -4
	classes['Check'][Search].flags = 4	Search = Search + 1
  end
     classes['dexs'] = gg.getValues(classes['dexs'])
     classes['Check'] = gg.getValues(classes['Check'])
      Search = 1
        for index, value in ipairs(classes['dexs']) do
     	if (classes['dexs'][index].value == 175662436) and (classes['Check'][index].value == 175662436) then
	     	classes['Verified'][Search] = {}
		    classes['Verified'][Search] =  classes['dexs'][index]
	    	Search = Search + 1
    	end
    end
    for index, value in ipairs(classes['Verified']) do
        classes['Verified'][index].address = classes['Verified'][index].address + 0
     	classes['Verified'][index].flags = 4
     end
     gg.loadResults(classes['Verified']) 

	local results = gg.getResults(gg.getResultsCount())
	
	local dexs = self:results2dexs(results)

	gg.clearResults()

	return dexs
end

function dumpDex:getDexs2()
	gg.clearResults()   
       
      local classes = {}
      classes['dexs'] = {}
      classes['Check'] = {}
      classes['Verified'] = {}
      Search = 1
      
      gg.searchNumber(3617584, 4) 
      
      local Results1 = gg.getResults(250)
      
    for index, value in ipairs(Results1) do   
    classes['dexs'][Search] = {}
    classes['dexs'][Search].address = Results1[index].address + -4
	classes['dexs'][Search].flags = 4
	classes['Check'][Search] = {}
	classes['Check'][Search].address = Results1[index].address + -4
	classes['Check'][Search].flags = 4	Search = Search + 1
  end
     classes['dexs'] = gg.getValues(classes['dexs'])
     classes['Check'] = gg.getValues(classes['Check'])
      Search = 1
        for index, value in ipairs(classes['dexs']) do
     	if (classes['dexs'][index].value == 175662436) and (classes['Check'][index].value == 175662436) then
	     	classes['Verified'][Search] = {}
		    classes['Verified'][Search] =  classes['dexs'][index]
	    	Search = Search + 1
    	end
    end
    for index, value in ipairs(classes['Verified']) do
        classes['Verified'][index].address = classes['Verified'][index].address + 0
     	classes['Verified'][index].flags = 4
     end
     gg.loadResults(classes['Verified'])
     
	local results = gg.getResults(gg.getResultsCount())
	local dexs = self:results2dexs2(results)
	gg.clearResults()
	return dexs
end

function dumpDex:getLogPath()
	return string.format('%s/dump.log', self:getDumpDir())
end

function dumpDex:getLogFile()
	return assert(io.open(self:getLogPath(), 'w'))
end

function dumpDex:start2()
	local function dumpAll(dexs)
		local log
		local ok, err = pcall(function()
			log = self:getLogFile()
		end)
		local function outLog(msg)
			msg = tostring(msg)
			if log then
				log:write(msg .. '\n')
			end
			if msg:find('%S') then
				gg.toast(msg)
			end
		end
		local msg = string.format('Export package name：%s', self:getTargetPackage())
		outLog(msg)
		local successCount = 0
		local failCount = 0
		for i, dex in ipairs(dexs) do
			local name = dex:getName()
			local msg = string.format('Exporting：%s', name)
			outLog(msg)
			local path, err = dex:out()
			if not path then
				failCount = failCount + 1
				local msg = string.format('Export failed：%s', err)
				outLog(msg)
			else
				successCount = successCount + 1
				local msg = string.format('Export successful：%s', path)
				outLog(msg)
				local msg = string.format('File size：%s', dex:getSize())
				outLog(msg)
			end
			outLog('\n')
		end
		local msg = string.format('Exported successfully %s 个DEX', successCount)
		if failCount > 0 then
			msg = msg .. '\n' .. string.format('Export failed %s 个DEX', failCount)
		end
		msg = msg .. '\n' .. string.format('saved on path %s', self:getDumpDir())
		outLog(msg)
		gg.alert(msg)
		if log then
			log:close()
		end
	end
	local startTime = os.clock()
	self:setPackageName(self:getTargetPackage())
	local dexs = self:getDexs2()
	local consuming = os.clock() - startTime
	local dexCount = #dexs
	local msg = string.format('It took %.2fs to search %d dex files in the memory.', consuming, dexCount)
	local operationNames = {'Export everything with one click'}
	local operationFuns = {}
	operationFuns[1] = function()
		return dumpAll(dexs)
	end
	for i, dex in ipairs(dexs) do
		local name = dex:getName()
		local text = name .. '\n' .. dex:getSize() .. 'Size'
		local i = #operationNames + 1
		operationNames[i] = text
		operationFuns[i] = function()
			local path, err = dex:out()
			if not path then
				gg.alert(string.format('%sExport failed! \n\n%s', name, err))
				return
			end

			gg.alert(string.format('%sExport successful! \n\n%s', name, path))
		end
	end
	while true do
		if gg.isVisible() then
			local input = gg.choice(operationNames, nil, msg)
			if not input then
				local input2 = gg.alert('Are you sure to quit? ', 'Sure', 'No')
				if input2 == 1 then
					return
				else
					gg.setVisible(false)
				end
			else
				local func = operationFuns[input]
				self:trySelfCall(func)
			end
		else
			gg.sleep(100)
		end
	end
end

function dumpDex:start3()

    gg.alert('Note This function dump Dex for Applications who have libdexprotector.so , so it will not work for other Dexs')
    
    gg.clearResults()   
       
      local classes = {}
      classes['dexs'] = {}
      classes['Check'] = {}
      classes['Verified'] = {}
      Search = 1      
      gg.setRanges(32)
      gg.searchNumber(3486512, 4) 
      
      local Results1 = gg.getResults(250)
      
    for index, value in ipairs(Results1) do   
    classes['dexs'][Search] = {}
    classes['dexs'][Search].address = Results1[index].address
	classes['dexs'][Search].flags = 4
	classes['Check'][Search] = {}
	classes['Check'][Search].address = Results1[index].address
	classes['Check'][Search].flags = 4	Search = Search + 1
  end
     classes['dexs'] = gg.getValues(classes['dexs'])
     classes['Check'] = gg.getValues(classes['Check'])
      Search = 1
        for index, value in ipairs(classes['dexs']) do
     	if (classes['dexs'][index].value == 3486512) and (classes['Check'][index].value == 3486512) then
	     	classes['Verified'][Search] = {}
		    classes['Verified'][Search] =  classes['dexs'][index]
	    	Search = Search + 1
    	end
    end
    for index, value in ipairs(classes['Verified']) do
        classes['Verified'][index].address = classes['Verified'][index].address + -4
     	classes['Verified'][index].flags = 4
     end
     gg.loadResults(classes['Verified'])
   
    local do_to = 175662436 
   
     gg.getResults(1000)

 	 gg.editAll(do_to, 4)
	
     local resultCounts = gg.getResultsCount()


     local results = gg.getResults(resultCounts)
    
    gg.clearResults()

    for i=1 , resultCounts do
    
    STADDR = results[i].address
  
    local dexs = {}
    dexs[1] = {}
    dexs[1].address = STADDR + 4
    dexs[1].flags = 4
    dexs = gg.getValues(dexs)
    if dexs[1].value == 3486512 then
  
     local checkSize = {}
     checkSize[1] = {}
     checkSize[1].address = STADDR + 32
     checkSize[1].flags = 4
     checkSize = gg.getValues(checkSize)
     capture = checkSize[1].value
    
     ENADDR = checkSize[1].address + capture
     packageName = gg.getTargetPackage()
     gg.dumpMemory(STADDR,ENADDR,"/storage/emulated/0/dumpDex/".. packageName)
     
     gg.alert('the dexs saved in /sdcard/dumpDex/\n If you see .bin files, know that the dump was completed successfully. You must now go to repair the header with MT Manager or NP Manager\n\n\nVery important information before you repair the dex head\n Maybe bin have two heads on top of each other. Find the second head through hex and separate it from the first head to get the second dex.')
   end
 end
end

function dumpDex:start()

	local function dumpAll(dexs)
		local log
		local ok, err = pcall(function()
			log = self:getLogFile()
		end)

		-- if not ok then
		-- 	if gg.alert(string.format('Unable to create LOG file\n%s', err), 'continue', 'quit') ~= 1 then
		-- 		return
		-- 	end
		-- end

		local function outLog(msg)
			msg = tostring(msg)

			if log then
				log:write(msg .. '\n')
			end

			if msg:find('%S') then
				gg.toast(msg)
			end
		end

		local msg = string.format('Export package name：%s', self:getTargetPackage())
		outLog(msg)

		local successCount = 0
		local failCount = 0

		for i, dex in ipairs(dexs) do
			local name = dex:getName()
			local msg = string.format('Exporting：%s', name)
			outLog(msg)

			local path, err = dex:out()
			if not path then
				failCount = failCount + 1
				local msg = string.format('Export failed：%s', err)
				outLog(msg)
			else
				successCount = successCount + 1
				local msg = string.format('Export successful：%s', path)
				outLog(msg)

				local msg = string.format('File size：%s', dex:getSize())
				outLog(msg)
			end
			outLog('\n')
		end

		local msg = string.format('Exported successfully %s 个DEX', successCount)
		if failCount > 0 then
			msg = msg .. '\n' .. string.format('Export failed %s 个DEX', failCount)
		end
		msg = msg .. '\n' .. string.format('saved on path %s', self:getDumpDir())

		outLog(msg)

		gg.alert(msg)

		-- Close LOG file
		if log then
			log:close()
		end
	end


	local startTime = os.clock()

	-- Cache package names to avoid package name inconsistencies caused by process switching
	self:setPackageName(self:getTargetPackage())

	-- Get DEX object set
	local dexs = self:getDexs()

	-- Get the time it takes to parse DEX
	local consuming = os.clock() - startTime

	local dexCount = #dexs
	local msg = string.format('It took %.2fs to search %d dex files in the memory.', consuming, dexCount)

	local operationNames = {'Export everything with one click'}
	local operationFuns = {}
	operationFuns[1] = function()
		return dumpAll(dexs)
	end

	for i, dex in ipairs(dexs) do
		local name = dex:getName()
		local text = name .. '\n' .. dex:getSize() .. 'Size'
		local i = #operationNames + 1
		operationNames[i] = text

		operationFuns[i] = function()
			local path, err = dex:out()
			if not path then
				gg.alert(string.format('%sExport failed! \n\n%s', name, err))
				return
			end

			gg.alert(string.format('%sExport successful! \n\n%s', name, path))
		end
	end

	while true do
		if gg.isVisible() then
			local input = gg.choice(operationNames, nil, msg)
			if not input then
				local input2 = gg.alert('Are you sure to quit? ', 'Sure', 'No')
				if input2 == 1 then
					return
				else
					gg.setVisible(false)
				end
			else
				local func = operationFuns[input]
				self:trySelfCall(func)
			end
		else
			gg.sleep(100)
		end
	end
end

function dumpDex:try(err)
	gg.alert(string.format('try error:\n%s', err))
	return err
end

function dumpDex:trySelfCall(func, ...)
	local ok, err = pcall(func, self, ...)
	if not ok then
		self:try(err)
	end
end

function dumpDex:main()

	local function getMsg()
		local process = string.format('Package：%s', self:getTargetPackage())
		local range = string.format('Memory：%s', self:getRangeText())
		local msg = process .. '\n' .. range
		return msg
	end
	
	gg.setVisible(false)
	while true do
		if gg.isVisible() then
		gg.setVisible(false)
			local input = gg.choice({'Select memory', 'Start export head 035', 'Start export head 037', 'DexProtector Dump', 'exit the program'}, nil, getMsg())
			if not input then
				gg.setVisible(false)

			elseif input == 1 then
				self:trySelfCall(self.selectRange)

			elseif input == 2 then
				self:trySelfCall(self.start)
				
			elseif input == 3 then
				self:trySelfCall(self.start2)
				
			elseif input == 4 then
				self:trySelfCall(self.start3)

			elseif input == 5 then
				return
			end
		else
			gg.sleep(100)
		end
	end
	
end

dumpDex:main()