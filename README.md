# getTotp
I like to use keyboard shortcut, therefore, I developed this script in order to save my TOTP in one place.

Using the MAC, I used software in order to use it, it can be Raycast, hammerspoon, expanso, or others

I like Raycast and a lighter version hammerspoon

This is the init.lua for hammerspon to associate (ALT/OPTION)+1

````
hs.hotkey.bind({"alt" }, "1", function()
hs.alert.closeAll()
  hs.alert.show("OTP UdeM Copiée en mémoire!")
ok,result = hs.applescript('do shell script "/usr/bin/python3 ~/getTotp.py -c"')
ok,result = hs.applescript('do shell script "/usr/bin/python3 ~/getTotp.py"')
    hs.alert.show(result,hs.styledtext,hs.screen.mainScreen(),10 )
end)
`````

In Windows you can create a shortcut and associate some key to run it in linux too
