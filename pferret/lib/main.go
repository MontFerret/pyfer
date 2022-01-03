package main

/*
struct COptions {
	char* cdp;
	char* proxy;
	char* user_agent;
};

struct CResult {
    char* data;
    char* err;
};
*/
import "C"

import (
	"context"
	"github.com/MontFerret/ferret"
	"github.com/MontFerret/ferret/pkg/drivers"
	"github.com/MontFerret/ferret/pkg/drivers/cdp"
	"github.com/MontFerret/ferret/pkg/drivers/http"
)

type Options struct {
	Cdp       string
	Params    map[string]interface{}
	Proxy     string
	UserAgent string
}

//export Execute
func Execute(queryC *C.char, optsC C.struct_COptions) C.struct_CResult {
	query := C.GoString(queryC)

	opts := Options{}
	cdpS := C.GoString(optsC.cdp)

	if len(cdpS) != 0 {
		opts.Cdp = cdpS
	}

	proxyS := C.GoString(optsC.proxy)

	if len(proxyS) != 0 {
		opts.Proxy = proxyS
	}

	userAgentS := C.GoString(optsC.user_agent)

	if len(userAgentS) != 0 {
		opts.UserAgent = userAgentS
	}

	f := ferret.New()
	err := f.Drivers().Register(http.NewDriver(
		http.WithProxy(opts.Proxy),
		http.WithUserAgent(opts.UserAgent),
	), drivers.AsDefault())

	if err != nil {
		return C.struct_CResult{
			err: C.CString(err.Error()),
		}
	}

	err = f.Drivers().Register(cdp.NewDriver(
		cdp.WithProxy(opts.Proxy),
		cdp.WithUserAgent(opts.UserAgent),
		cdp.WithAddress(opts.Cdp),
	))

	if err != nil {
		return C.struct_CResult{
			err: C.CString(err.Error()),
		}
	}

	out, err := f.Exec(
		context.Background(),
		query,
		//runtime.WithParams(opts.Params),
	)

	if err != nil {
		return C.struct_CResult{
			err: C.CString(err.Error()),
		}
	}

	return C.struct_CResult{
		data: C.CString(string(out)),
	}
}

func main() {

}
