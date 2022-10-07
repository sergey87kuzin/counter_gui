def frame_button_click(stock, entries, button):
    stock.start()
    stock.root.children[button].invoke()
    for entry in entries:
        stock.frame.children[entry[0]].delete(0, 'end')
        stock.frame.children[entry[0]].insert(0, entry[1])
    stock.frame.children[button].invoke()
