package main

import "C"
import (
	"context"
	"os"
	"os/signal"

	"github.com/MontFerret/ferret/pkg/compiler"
	"github.com/MontFerret/ferret/pkg/drivers"
	"github.com/MontFerret/ferret/pkg/drivers/cdp"
	"github.com/MontFerret/ferret/pkg/drivers/http"
)

type Options struct {
	Cdp         string
	Params      map[string]interface{}
	Proxy       string
	UserAgent   string
	ShowTime    bool // TODO: not used
	KeepCookies bool // TODO: not used
}

func (opts Options) WithContext(ctx context.Context) (context.Context, context.CancelFunc) {
	httpDriver := http.NewDriver()

	ctx = drivers.WithContext(
		ctx,
		httpDriver,
		drivers.AsDefault(),
	)

	cdpOpts := []cdp.Option{
		cdp.WithAddress(opts.Cdp),
	}

	cdpDriver := cdp.NewDriver(cdpOpts...)

	ctx = drivers.WithContext(
		ctx,
		cdpDriver,
	)

	return context.WithCancel(ctx)
}

//export Execute
func Execute(queryC *C.char, cdpC, proxyC, userAgentC *C.char) *C.char {
    // TODO: add namesC *[]*C.char, valuesC *[]*C.char
	query := C.GoString(queryC)

	opts := Options{}
	cdpS := C.GoString(cdpC)
	if len(cdpS) != 0 {
		opts.Cdp = cdpS
	}
	proxyS := C.GoString(proxyC)
	if len(proxyS) != 0 {
		opts.Proxy = proxyS
	}
	userAgentS := C.GoString(userAgentC)
	if len(userAgentS) != 0 {
		opts.UserAgent = userAgentS
	}

	ferret := compiler.New()

	prog, err := ferret.Compile(query)

	if err != nil {
		return C.CString("Failed to compile the query")
	}

	ctx, cancel := opts.WithContext(context.Background())

	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)
	signal.Notify(c, os.Kill)

	go func() {
		for {
			<-c
			cancel()
		}
	}()

	out, err := prog.Run(
		ctx,
		//runtime.WithParams(opts.Params),
	)

	if err != nil {
		return C.CString("Failed to execute the query")
	}

	return C.CString(string(out))
}

func main() {

}
