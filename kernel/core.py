# Derived from https://github.com/wasmerio/wasmer-python/blob/master/examples/engine_jit.py

from wasmer import engine, wat2wasm, Store, Module, Instance
from wasmer_compiler_cranelift import Compiler


def get_code():

    # Let's declare the Wasm module with the text representation.
    wasm_bytes = wat2wasm(
        """
        (module
          (type $sum_t (func (param i32 i32) (result i32)))
          (func $sum_f (type $sum_t) (param $x i32) (param $y i32) (result i32)
            local.get $x
            local.get $y
            i32.add)
          (export "add" (func $sum_f)))
        """
    )
    return wasm_bytes


def run_code(wasm_code):

    # Define the engine that will drive everything.
    #
    # In this case, the engine is `wasmer.engine.JIT` which roughly
    # means that the executable code will live in memory.
    wasmer_engine = engine.JIT(Compiler)

    # Create a store, that holds the engine.
    store = Store(wasmer_engine)

    # Here we go.
    #
    # Let's compile the Wasm module. It is at this step that the Wasm text
    # is transformed into Wasm bytes (if necessary), and then compiled to
    # executable code by the compiler, which is then stored in memory by
    # the engine.
    module = Module(store, wasm_code)

    # Congrats, the Wasm module is compiled! Now let's execute it for the
    # sake of having a complete example.
    #
    # Let's instantiate the Wasm module.
    instance = Instance(module)

    # The Wasm module exports a function called `sum`.
    add = instance.exports.add
    results = add(1, 2)

    print(results)


def main():
    code = get_code()
    run_code(code)


if __name__ == "__main__":
    main()
