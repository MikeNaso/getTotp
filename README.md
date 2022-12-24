# getTotp
I like to use keyboard shortcut, therefore, I developed this script in order to save my TOTP in one place.

I use a Mac in my day-to-day work,  therefore here some good software in order to better manage key shortcut and much more: Raycast, hammerspoon, expanso, or others

I like Raycast or hammerspoon (much fewer options but good for this kind of utilization)

This is the init.lua for hammerspon to associate (ALT/OPTION)+1 (Click on the menu for editing)

````
hs.hotkey.bind({"alt" }, "1", function()
hs.alert.closeAll()
  hs.alert.show("OTP UdeM Copiée en mémoire!")
ok,result = hs.applescript('do shell script "/usr/bin/python3 ~/getTotp.py -c"')
ok,result = hs.applescript('do shell script "/usr/bin/python3 ~/getTotp.py"')
    hs.alert.show(result,hs.styledtext,hs.screen.mainScreen(),10 )
end)
`````

In Windows you can create a shortcut and associate some key to run it in Linux the same.
