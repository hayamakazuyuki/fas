function initPostcodeJp() {

    // APIキーを指定して住所補完サービスを作成
    var postcodeJp = new postcodejp.address.AutoComplementService('qPSsc4Hnc2wScb0W8v546Cp8RuuK1Eg0DLjuZvu');

    // 郵便番号テキストボックスを指定
    postcodeJp.setZipTextbox('zip')

    // 住所補完フィールドを追加
    postcodeJp.add(new postcodejp.address.StateTextbox('prefecture'));
    postcodeJp.add(new postcodejp.address.TownTextbox('city'));
    postcodeJp.add(new postcodejp.address.StreetTextbox('town'));

    // 郵便番号テキストボックスの監視を開始
    postcodeJp.observe();

  }
  if(window.addEventListener){
    window.addEventListener('load', initPostcodeJp)
  }else{
    window.attachEvent('onload', initPostcodeJp)
  }
