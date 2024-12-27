$(document).ready(function () {
    console.log("updated successfully setup");
    const fm$ = $("form.address_form_update");
    const fmBtn$ = fm$.find("button[type=submit]");
    const phoneQueryUrl = "/partials/query-phone-number/"

    fm$.find("input[name=phone_number]").on("input", function (event) {
        const val = $(event.target).val();
        $.getJSON(`${phoneQueryUrl}?phone_number=${val}`).done(function (response) {
            const { phone_present } = response;
            if (!phone_present) {
                if (val.trim().length > 9) {
                    fmBtn$.prop("disabled", true);
                }
                fmBtn$.prop("disabled", true);
            }
            fmBtn$.prop("disabled", false);
        }).fail((xhr, status, errorThrown) => {

        })
    })

    fm$.submit(function (event) {
        event.preventDefault();
        const fd = new FormData(this);
        fmBtn$.text("updating address ...")
        fmBtn$.prop("disabled", true);
        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            processData: false,
            contentType: false,
            data: fd,
            success: function (data) {
                console.log(data);
                fmBtn$.text("update successful")
            },
            error: function (xhr, status, error) {
                console.log(xhr.responseJSON)
                const { message } = xhr.responseJSON
                fmBtn$.text(message)
            },
            complete: function () {
                setTimeout(() => {
                    fmBtn$.text("update address")
                    fmBtn$.prop("disabled", false);
                }, 5000);
            }
        })
    });
});
