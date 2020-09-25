from idaapi import *
denger_funcs = ["strcpy", "sprinf", "strncpy"]

for func in danger_funcs:
	addr = LocByName(func)
	if addr != BADADDR:
		# Grap the cross-references to this address
		cross_ref = CodeRefsTo(addr, 0)
		print("Cross References to %s" % (func))
		print("-------------------------------")
		for ref in cross_ref:
			print("%08x" % (ref))
			# Color the call RED
			SetColor(ref, CIC_ITEM, 0x0000ff)
			
