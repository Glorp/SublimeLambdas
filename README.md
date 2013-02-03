Lambda Things for Sublime Text 3
================================

Lets you write untyped lambda calculus-expressions in Sublime Text 3 and do lambda calculus-things to them. Useful.

(for Sublime Text 2, goto [here](https://github.com/Glorp/SublimeLambdas/tree/ST2))

Setup
-----

Get lambda.py and put it somewhere. (some Sublime place)/Packages/User/ seems fine.

And then you maybe want to make some keys do some of the lambdathings. Me, personally, for myself, I have put this in one .sublime-keymap or another:

    { "keys": ["ctrl+shift+x"], "command": "lambda_reduce" },
    { "keys": ["ctrl+shift+c"], "command": "lambda_reduce_lots" },
    { "keys": ["ctrl+shift+r"], "command": "lambda_replace_names" },
    { "keys": ["ctrl+l"], "command": "insert", "args": {"characters": "λ"} },

I'm sure this collides horribly with all the keybindings real Sublime people use and you absolutely should not use those keys. But you maybe should use those commands, because those are the commands.

Evaluating/reducing things
--------------------------

Now you can write great things like

    (λa.λb.a (b (λn.λf.λx.f (n f x))) (λf.λx.x)) (λf.λx.f (f (f x))) (λf.λx.f (f x))

, and run `lambda_reduce` (`ctrl+shift+x`, or *something*) to du beta reduction. That will make it put

    (λb.(λf.λx.f (f (f x))) (b (λn.λf.λx.f (n f x))) (λf.λx.x)) (λf.λx.f (f x))

on the next line. If you get tired of doing `lambda_reduce` over and over and wanna do beta reduce like a lot, you can do `lambda_reduce_lots` (`ctrl+shift+c`):


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

you can do `lambda_replace_names` (`ctrl+shift+r`) and it will put

    (λn.λf.λx.f (n f x)) ((λn.λf.λx.f (n f x)) (λf.λx.x))

on the next line. And then you can reduce things from there:

    λf.λx.f ((λn.λf.λx.f (n f x)) (λf.λx.x) f x)
    λf.λx.f ((λf.λx.f ((λf.λx.x) f x)) f x)
    λf.λx.f ((λx.f ((λf.λx.x) f x)) x)
    λf.λx.f (f ((λf.λx.x) f x))
    λf.λx.f (f ((λx.x) x))
    λf.λx.f (f x)

Is two!

There are some names and things [here](https://gist.github.com/4026290).

Details
-------

All the commands read the line your cursor is on. If you have cursors all over the place, it probably just picks the first one. After writing things it will move the cursor to the end of what it wrote. If you put a `|` somewhere in a line, everything from there till the end of the line will be ignored.

`lambda_replace_names` is pretty much just copypasting. It will add parentheses to make sure the named things won't get mixed up with their surroundings, but it won't deal with scoping. If your named things have free variables, you can capture those. And if you're using the name of a named thing as a bound variable, that will not keep it from getting replaced by that thing.

`lambda_reduce_lots` stops if nothing can be reduced. Or if it has printed like a thousand lines.

Variables will sometimes be renamed in order to avoid naming conflicts/crazy scoping. That's going to look like so:

    λy.(λx.λy.x y) y | y -> y1
    λy1.(λx.λy.x y) y1
    λy1.λy.y1 y

It adds the `| y -> y1` bit to the line before the one where the variable is renamed. The line with the renaming only does renaming, no reducing.
