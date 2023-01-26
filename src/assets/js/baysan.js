const get_notification = (message, status) => {
    /*
        * message (str) : Message text
        * status (str)  : Message badge color flag (success, error, warning and other bootstrap identifiers)
     */
    $('#messageToast').remove();

    $('body').append(`
        <div class="toast-container position-fixed bottom-0 end-0 p-3">
            <div id="messageToast" class="toast align-items-center" role="alert" aria-live="assertive"
                 aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        <span class="badge text-bg-${status}"> </span>
                        ${message}
                    </div>
                    <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        </div>
    `);
    const toastLiveExample = document.getElementById('messageToast')
    const toast = new bootstrap.Toast(toastLiveExample)
    toast.show()
}