
$(document).ready(function () {
    console.log("Loading instructor setup ...");

    function _handleRequest(fm, data) {
        const fmBtn$ = fm.find("button[type=submit]");
        const btnText$ = fmBtn$.find("span.btn-text");
        const response$ = fm.find("div#response");

        fmBtn$.prop("disabled", true);
        btnText$.text("initiating payout request...");

        $.ajax({
            type: fm.attr("method"),
            url: fm.attr("action"),
            data: data,
            processData: false,
            contentType: false,
            success: function (response) {
                const { message } = response
                btnText$.text("Initiation of payout completed successfully")
                response$.addClass("mt-3 alert alert-success").text(message)
            },
            error: function (xhr, status, err) {
                btnText$.text(err);
                const { message } = xhr.responseJSON;
                response$.addClass("mt-3 alert alert-danger").text(message)
            },
            complete: function () {
                fmBtn$.prop("disabled", false);
                btnText$.text("proceed with payout");
                setTimeout(() => {
                    response$.removeAttr("class").text("");
                }, 10000)
            },
        })
    }
    const fm$ = $("form#processPayoutForm")
    const fmBtn$ = fm$.find("button[type=submit]");

    fm$.find("input[name=amount]").on("input", function (event) {
        const amount = $(event.target).val();
        const small$ = $(this).closest("small")
        console.log(amount);
        if (parseInt(amount) < 55) {
            fmBtn$.prop("disabled", true);
        } else {
            fmBtn$.prop("disabled", false);
        }
        $.getJSON(`${$(this).attr("hx-url")}?amount=${amount}`).done(function (response) {
            const { enough } = response;
            if (!enough) {
                fmBtn$.prop("disabled", true);
                small$.text(`Insufficient funds to withdraw $${amount}. Need to cover also the fee`);
            } else {
                fmBtn$.prop("disabled", false);
                small$.text("Min withdrawable amount $55.00")
            }
        }).fail(function (xhr, status, error) {
            small$.text("Error loading withdrawable amount");

            setTimeout(() => {
                small$.text("Min withdrawable amount $55.00")
            }, 5000);
        });
    })

    fm$.submit(function (event) {
        event.preventDefault();
        const fd = new FormData(this)
        _handleRequest(fm$, fd);
    })
});