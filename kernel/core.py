# Derived from
# https://github.com/wasmerio/wasmer-python/blob/1.0.0-beta1/examples/engine_jit.py
# https://github.com/wasmerio/wasmer-python/blob/1.0.0-beta1/examples/imports_function.py
import sys
from wasmer import engine, wat2wasm, Store, Module, Instance, ImportObject, Function
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


def load_code(filename):
    wasm_bytes = wat2wasm(open(filename, "r").read())
    return wasm_bytes


def host_functions(store: Store) -> ImportObject:
    """
    Provide an "abort()" host function.
    https://github.com/flow-heater/pytshello/issues/1

    :param store:
    :return:
    """

    # When creating an `Instance`, we can pass an `ImportObject`. All
    # entities that must be imported are registered inside the
    # `ImportObject`.
    import_object = ImportObject()

    # Let's write the Python function that is going to be imported,
    # i.e. called by the WebAssembly module.
    def abort(a: 'i32', b: 'i32', c: 'i32', d: 'i32'):
        pass

    abort_host_function = Function(store, abort)

    # Now let's register the `sum` import inside the `env` namespace.
    import_object.register(
        "env",
        {
            "abort": abort_host_function,
        }
    )

    return import_object


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

    # Provide an "abort()" host function.
    import_object = host_functions(store)

    # Congrats, the Wasm module is compiled! Now let's execute it for the
    # sake of having a complete example.
    #
    # Let's instantiate the Wasm module.
    instance = Instance(module, import_object)

    # The Wasm module exports a function called `sum`.
    add = instance.exports.add
    results = add(1, 2)

    print(results)


def main():
    what = sys.argv[1]
    if what == "inline":
        code = get_code()
    elif what == "typescript":
        code = load_code("userspace-typescript/build/untouched.wat")
    else:
        raise ValueError("Undefined invocation")
    run_code(code)


if __name__ == "__main__":
    main()
