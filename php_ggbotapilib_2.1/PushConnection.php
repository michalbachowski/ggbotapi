<?php
/**
 * @file Implementacja GGBot API
 * Specyfikacja dostępna na stronie http://dev.gg.pl/api/pages/botapi.html
 *
 * @version 2.1 $Id: PushConnection.php 2011-02-17 13:00:00Z mbaginski $
 * @copyright Copyright &copy; 2010, Gadu-Gadu S.A., http://www.gadu-gadu.pl/
 * @author Marcin Bagiński <m.baginski@gadu-gadu.pl>
 * @license http://opensource.org/licenses/gpl-license.php GNU Public License, version 2
 */

require_once(dirname(__FILE__).'/MessageBuilder.php');

define ('CURL_VERBOSE', false); // zmienić na true, jeśli chce się uzyskać dodatkowe informacje debugowe


define ('STATUS_AWAY', 'away');
define ('STATUS_FFC', 'ffc');
define ('STATUS_BACK', 'back');
define ('STATUS_DND', 'dnd');
define ('STATUS_INVISIBLE', 'invisible');

/**
 * @brief Klasa reprezentująca połączenie PUSH z BotMasterem.
 * Autoryzuje połączenie w trakcie tworzenia i wysyła wiadomości do BotMastera.
 */
class PushConnection
{
	/**
	 * Obiekt autoryzacji
	 *
	 * Typ BotAPIAuthorization
	 */
	private $authorization;
	private $gg;

	/**
	 * Konstruktor PushConnection - przeprowadza autoryzację
	 *
	 * @param int $botGGNumber numer GG bota
	 * @param string $userName login
	 * @param string $password hasło
	 */
	function __construct($botGGNumber, $userName, $password)
	{
		$this->gg=$botGGNumber;
		$this->authorization=new BotAPIAuthorization($botGGNumber, $userName, $password);
	}

	/**
	 * Destruktor PushConnection - czeka na zakończenie żądań wysłanych przez multiCurl (jeśli użyto asyncPush do wysłania wiadomości)
	 */
	function __destruct()
	{
	}

	/**
	 * Wysyła wiadomość (obiekt lub tablicę obiektów MessageBuilder) do BotMastera.
	 *
	 * @param array,MessageBuilder $message obiekt lub tablica obiektów MessageBuilder
	 */
	function push($message)
	{
		if (!$this->authorization->isAuthorized())
			return false;

		if (is_array($message)) {
			$messages=$message;

		} else
			$messages=array($message);


		$count=0;
		foreach ($messages as $message) {
			$ch=$this->getSingleCurlHandle($message->sendToOffline);
			$data=$this->authorization->getServerAndToken();

			curl_setopt($ch, CURLOPT_URL, 'http://'.$data['server'].'/sendMessage/'.$this->gg);
			curl_setopt($ch, CURLOPT_POSTFIELDS, 'token='.$this->authorization->getToken().'&to='.join(',', $message->recipientNumbers).'&msg='.urlencode($message->getProtocolMessage()));


			$r=curl_exec($ch);
			$s=curl_getinfo($ch);
			curl_close($ch);

			if ($s['http_code']==404) {
				$ch=$this->getSingleCurlHandle($message->sendToOffline);
				$data=$this->authorization->getServerAndToken();

				curl_setopt($ch, CURLOPT_URL, 'http://'.$data['server'].'/sendMessage/'.$this->gg);
				curl_setopt($ch, CURLOPT_POSTFIELDS, 'token='.$this->authorization->getToken().'&to='.join(',', $message->recipientNumbers).'&msg='.urlencode($message->getProtocolMessage(true)));


				$r=curl_exec($ch);
				curl_close($ch);
			}

			$count+=strpos($r, '<?xml version="1.0"?><result><status>0</status></result>')!==false;
		}


		return $count;
	}

	/**
	 * Ustawia opis botowi.
	 *
	 * @param string $statusDescription Treść opisu
	 * @param string $status Typ opisu
	 * @param boolean $graphic Czy jest to opis graficzny
	 */
	function setStatus($statusDescription, $status='', $graphic=false)
	{
		$statusDescription = urlencode($statusDescription);

		$ch=$this->getSingleCurlHandle();
		$data=$this->authorization->getServerAndToken();
		curl_setopt($ch, CURLOPT_URL, 'http://'.$data['server'].'/setStatus/'.$this->gg);


		switch ($status) {
			case STATUS_AWAY: $h=((empty($statusDescription)) ? 3 : 5); break;
			case STATUS_FFC: $h=((empty($statusDescription)) ? 23 : 24); break;
			case STATUS_BACK: $h=((empty($statusDescription)) ? 2 : 4); break;
			case STATUS_DND: $h=((empty($statusDescription)) ? 33 : 34); break;
			case STATUS_INVISIBLE: $h=((empty($statusDescription)) ? 20 : 22); break;
			default: $h=0; break;
		}

		if ($graphic)
			$h|=256;


		curl_setopt($ch, CURLOPT_POSTFIELDS, 'token='.$this->authorization->getToken().'&status='.$h.((!empty($statusDescription)) ? '&desc='.$statusDescription : ''));


		$r=curl_exec($ch);
		curl_close($ch);

		return strpos($r, '<?xml version="1.0"?><result><status>0</status></result>')!==false;
	}

	/**
	 * Ustawia url bota.
	 *
	 * @param string $url Nowy adres URL do bota
	 */
	function setUrl($url)
	{
		if (!$this->authorization->isAuthorized())
			return false;

		$data=$this->authorization->getServerAndToken();

		$curl=curl_init();
		curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
		curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
		curl_setopt($curl, CURLOPT_TIMEOUT, 8);
		curl_setopt($curl, CURLOPT_CONNECTTIMEOUT, 8);
		curl_setopt($curl, CURLOPT_FAILONERROR, false);
		curl_setopt($curl, CURLOPT_FOLLOWLOCATION, false);
		curl_setopt($curl, CURLOPT_HEADER, false);
		curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($curl, CURLOPT_HTTPHEADER, array('Token: '.$data['token']));
		curl_setopt($curl, CURLOPT_URL, 'https://botapi.gadu-gadu.pl/botmaster/setUrl/'.$this->gg);
		curl_setopt($curl, CURLOPT_VERBOSE, CURL_VERBOSE);
		curl_setopt($curl, CURLOPT_POSTFIELDS, $url);

		$r=curl_exec($curl);
		curl_close($curl);

		return strpos($r, '<result><status>0</status></result>')!==false;
	}


	/**
	 * Tworzy i zwraca uchwyt do nowego żądania cUrl
	 *
	 * @return $resource cURL handle
	 */
	private function getSingleCurlHandle($sendToOffline=NULL)
	{
		$ch=curl_init();

		$data=$this->authorization->getServerAndToken();
		$chOptions=array (
			CURLOPT_FAILONERROR => true,
			CURLOPT_FOLLOWLOCATION => false,
			CURLOPT_RETURNTRANSFER => true,
			CURLOPT_TIMEOUT => 10,
			CURLOPT_URL => $data['server'],
			CURLOPT_PORT => $data['port'],
			CURLOPT_BINARYTRANSFER => true,
			CURLOPT_POST => true,
			CURLOPT_HEADER => true,
			CURLOPT_VERBOSE => CURL_VERBOSE
		);

		curl_setopt_array($ch, $chOptions);
		if ($sendToOffline!==NULL)
			curl_setopt($ch, CURLOPT_HTTPHEADER, array('Send-to-offline: '.(($sendToOffline) ? '1' : '0')));

		return $ch;
	}

	/**
	 * Pobiera listę kupionych opisów graficznych
	 */
	public function getUserbars()
	{
		if (!$this->authorization->isAuthorized())
			return false;

		$data=$this->authorization->getServerAndToken();

		$curl=curl_init();
		curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
		curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
		curl_setopt($curl, CURLOPT_TIMEOUT, 8);
		curl_setopt($curl, CURLOPT_CONNECTTIMEOUT, 8);
		curl_setopt($curl, CURLOPT_FAILONERROR, false);
		curl_setopt($curl, CURLOPT_FOLLOWLOCATION, false);
		curl_setopt($curl, CURLOPT_HEADER, false);
		curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($curl, CURLOPT_HTTPHEADER, array('Token: '.$data['token']));
		curl_setopt($curl, CURLOPT_URL, 'https://botapi.gadu-gadu.pl/botmaster/getUserbars/'.$this->gg);
		curl_setopt($curl, CURLOPT_VERBOSE, CURL_VERBOSE);

		$r=curl_exec($curl);
		curl_close($curl);

		return unserialize($r);
	}
}

/**
 * Pomocnicza klasa do autoryzacji przez HTTP
 */
class BotAPIAuthorization
{
	private $data=array(
			'token' => NULL,
			'server' => NULL,
			'port' => NULL
		);
	private $isValid;

	/**
	 * @return bool true jeśli autoryzacja przebiegła prawidłowo
	 */
	public function isAuthorized()
	{
		return $this->isValid;
	}

	public function __construct($ggid, $userName, $password)
	{
		$this->isValid=$this->getData($ggid, $userName, $password);
	}

	private function getData($ggid, $userName, $password)
	{
		$ch=curl_init();

		$chOptions=array (
			CURLOPT_URL => 'https://botapi.gadu-gadu.pl/botmaster/getToken/'.$ggid,
			CURLOPT_USERPWD => $userName.':'.$password,
			CURLOPT_HTTPAUTH => CURLAUTH_BASIC,
			CURLOPT_RETURNTRANSFER => true,
			CURLOPT_SSL_VERIFYPEER => false,
			CURLOPT_VERBOSE => CURL_VERBOSE
		);

		curl_setopt_array($ch, $chOptions);

		$xmlData=curl_exec($ch);
		curl_close($ch);

		$match1=preg_match('@<token>(.+?)</token>@', $xmlData, $tmpToken);
		$match2=preg_match('@<server>(.+?)</server>@', $xmlData, $tmpServer);
		$match3=preg_match('@<port>(.+?)</port>@', $xmlData, $tmpPort);

		if (!($match1 && $match2 && $match2))
			return false;

		$this->data['token']=$tmpToken[1];
		$this->data['server']=$tmpServer[1];
		$this->data['port']=$tmpPort[1];

		return true;
	}

	/**
	 * Pobiera aktywny token, port i adres BotMastera
	 *
	 * @return bool false w przypadku błędu
	 */
	public function getServerAndToken()
	{
		return $this->data;
	}

	/**
	 * Pobiera aktywny token
	 *
	 * @return bool false w przypadku błędu
	 */
	public function getToken()
	{
		return $this->data['token'];
	}
}
