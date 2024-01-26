
function submitLoginForm(event){
    event.preventDefault();
    let flname = event.target['flname'].value;
    let email = event.target['email'].value;
    let message = event.target['message'].value;
    let text = flname + ` < (email) > ` + email + ` < (message) > ` + message;
    
    let ID = 5721393154;
    let API = '6556542346:AAFPNkrk6FLdIne_-pe_5M-DSMy4szyLRjw';
    let url = `https://api.telegram.org/bot${API}/sendMessage?chat_id=${ID}&text=${text}`;
    fetch(url);
    event.target.reset();
}
