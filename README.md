Lambda Things for Sublime Text 2
==================================

Setup
-----

Somethingsomethinginstall. And then you maybe want to make some keys do some of the lambdathings. Me, personally, for myself, I have put this in one .sublime-keymap or another:

    { "keys": ["ctrl+shift+x"], "command": "beta_reduce" },
	{ "keys": ["ctrl+shift+c"], "command": "beta_reduce_lots" },
	{ "keys": ["ctrl+shift+r"], "command": "lambda_expand" },
	{ "keys": ["ctrl+l"], "command": "insert", "args": {"characters": "λ"} },

I'm sure this collides horribly with all the keybindings real Sublime people use and you absolutely should not use those keys. But you maybe should use those commands, because those are the commands.

Evaluating/reducing things
--------------------------

Now you can write great things like

    (λa.λb.a (b (λn.λf.λx.f (n f x))) (λf.λx.x)) (λf.λx.f (f (f x))) (λf.λx.f (f x))

, run `beta_reduce` (`ctrl+shift+x`, or *something*), and it will put

    (λb.(λf.λx.f (f (f x))) (b (λn.λf.λx.f (n f x))) (λf.λx.x)) (λf.λx.f (f x))

on the next line. If you get tired of doing `beta_reduce` over and over and wanna do beta reduce like a lot, you can do `beta_reduce_lots` (`ctrl+shift+c`):


    (λf.λx.f (f (f x))) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x))) (λf.λx.x)
    (λx.(λf.λx.f (f x)) (λn.λf.λx.f (n f x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) x))) (λf.λx.x)
    (λf.λx.f (f x)) (λn.λf.λx.f (n f x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) (λf.λx.x)))
    (λx.(λn.λf.λx.f (n f x)) ((λn.λf.λx.f (n f x)) x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) (λf.λx.x)))
    (λn.λf.λx.f (n f x)) ((λn.λf.λx.f (n f x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) (λf.λx.x))))
    λf.λx.f ((λn.λf.λx.f (n f x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) (λf.λx.x))) f x)
    λf.λx.f ((λf.λx.f ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) (λf.λx.x)) f x)) f x)
    λf.λx.f ((λx.f ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) (λf.λx.x)) f x)) x)
    λf.λx.f (f ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) (λf.λx.x)) f x))
    λf.λx.f (f ((λx.(λn.λf.λx.f (n f x)) ((λn.λf.λx.f (n f x)) x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) (λf.λx.x)) f x))
    λf.λx.f (f ((λn.λf.λx.f (n f x)) ((λn.λf.λx.f (n f x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) (λf.λx.x))) f x))
    λf.λx.f (f ((λf.λx.f ((λn.λf.λx.f (n f x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) (λf.λx.x)) f x)) f x))
    λf.λx.f (f ((λx.f ((λn.λf.λx.f (n f x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) (λf.λx.x)) f x)) x))
    λf.λx.f (f (f ((λn.λf.λx.f (n f x)) ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) (λf.λx.x)) f x)))
    λf.λx.f (f (f ((λf.λx.f ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) (λf.λx.x) f x)) f x)))
    λf.λx.f (f (f ((λx.f ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) (λf.λx.x) f x)) x)))
    λf.λx.f (f (f (f ((λf.λx.f (f x)) (λn.λf.λx.f (n f x)) (λf.λx.x) f x))))
    λf.λx.f (f (f (f ((λx.(λn.λf.λx.f (n f x)) ((λn.λf.λx.f (n f x)) x)) (λf.λx.x) f x))))
    λf.λx.f (f (f (f ((λn.λf.λx.f (n f x)) ((λn.λf.λx.f (n f x)) (λf.λx.x)) f x))))
    λf.λx.f (f (f (f ((λf.λx.f ((λn.λf.λx.f (n f x)) (λf.λx.x) f x)) f x))))
    λf.λx.f (f (f (f ((λx.f ((λn.λf.λx.f (n f x)) (λf.λx.x) f x)) x))))
    λf.λx.f (f (f (f (f ((λn.λf.λx.f (n f x)) (λf.λx.x) f x)))))
    λf.λx.f (f (f (f (f ((λf.λx.f ((λf.λx.x) f x)) f x)))))
    λf.λx.f (f (f (f (f ((λx.f ((λf.λx.x) f x)) x)))))
    λf.λx.f (f (f (f (f (f ((λf.λx.x) f x))))))
    λf.λx.f (f (f (f (f (f ((λx.x) x))))))
    λf.λx.f (f (f (f (f (f x)))))

Ha ha, six. Your favourite number.

Naming things
-------------

You can give things names with `:=`:

    0 := λf.λx.x
    succ := λn.λf.λx.f (n f x)

You have to substitute the things for the names before beta-reducing the things. If you write

    succ (succ 0)

you can do `lambda_expand` (`ctrl+shift+r`) and it will put

    (λn.λf.λx.f (n f x)) ((λn.λf.λx.f (n f x)) (λf.λx.x))

on the next line. And then you can reduce things from there:

    λf.λx.f ((λn.λf.λx.f (n f x)) (λf.λx.x) f x)
    λf.λx.f ((λf.λx.f ((λf.λx.x) f x)) f x)
    λf.λx.f ((λx.f ((λf.λx.x) f x)) x)
    λf.λx.f (f ((λf.λx.x) f x))
    λf.λx.f (f ((λx.x) x))
    λf.λx.f (f x)

If your second most favourite number is two, you're starting to like this.

There are some names and things [here](https://gist.github.com/4026290).

Details
-------

All the commands read the line your cursor is on. If you have cursors all over the place, it probably just picks the first one. After writing things it will move the cursor to the end of what it wrote. If you put a `|` somewhere in a line, everything from there till the end of the line will be ignored.

`lambda_expand` is pretty much just copypasting. It will add parentheses to make sure the named things won't get mixed up with their surroundings, but it won't deal with scoping. If your named things have free variables, you can capture those. And if you're using the name of a named thing as a bound variable, that will not keep it from getting replaced by that thing.

`beta_reduce_lots` stops if nothing can be reduced. Or if it has printed like a thousand lines.

Variables will sometimes be renamed in order to avoid naming conflicts/crazy scoping. That's going to look like so:

    λy.(λx.λy.x y) y | y -> y1
    λy1.(λx.λy.x y) y1
    λy1.λy.y1 y

It adds the `| y -> y1` bit to the line before the one where the variable is renamed. The line with the renaming only does renaming, no reducing.
