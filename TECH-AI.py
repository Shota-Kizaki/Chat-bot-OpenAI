import azure.cognitiveservices.speech as speechsdk
import openai
import os
import sys

from dotenv import load_dotenv
load_dotenv()

SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")
durable_task_url = os.getenv("durable_task_url")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

Hey = "Godfather"
table ="Godfather.table"

def recognize_from_microphone():
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_recognition_language = "ja-JP"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("質問をどうぞ")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("認識結果: {}".format(speech_recognition_result.text))
        data = speech_recognition_result.text
        if data == "終了。":
            print("終了します。")
            sys.exit()
        else:
            openai.api_key = AZURE_OPENAI_KEY
            openai.api_base = AZURE_OPENAI_ENDPOINT
            openai.api_type = 'azure'
            openai.api_version = '2023-03-15-preview'  # this may change in the future
            response = openai.ChatCompletion.create(
            engine="Kyoto-tech",
            messages = [{"role":"system","content":"あなたは京都テックのAIアシスタントです。50字程度に要約して返信してください。基本京都テックについて返信してください。会話文で返答して下さい。アシスタントらしい返答して下さい。以下を参照して下さい。"},{"role":"user","content":"京都テック(京都デザイン＆テクノロジー専門学校)"},{"role":"assistant","content":"京都テックとは、京都デザイン＆テクノロジー専門学校の略称。\n京都テックは京都府京都市下京区に校舎を構える専門学校。\n\n京都テックには全部で１８専攻あります。１８専攻がそれぞれ、ゲームワールド、esportsワールド、AI・IT・ロボットワールド、CG・映像ワールド、デザイン・イラストワールドの５つのワールドに分かれる。\n\nゲームワールドには４つの専攻がある。\n\n- スーパーゲームクリエイター専攻\n- ゲームプログラマー専攻\n- ゲーム企画シナリオ専攻\n- ゲームCG＆キャラクターデザイン専攻\n\nesportsワールドには２つの専攻がある。\n\n- esportsプロマネジメント専攻\n- esportsプロゲーマー専攻\n\nAI・IT・ロボットワールドには６つの専攻がある。\n\n- スーパーAIクリエイター専攻\n- データサイエンティスト専攻\n- ホワイトハッカー専攻\n- ロボット・Aiエンジニア専攻\n- スーパーITエンジニア専攻\n- ITプログラマー専攻\n\nCG・映像ワールドには４つの専攻がある。\n\n- スーパーCG映像クリエイター専攻\n- メタバースクリエイター専攻\n- ネット動画クリエイター専攻\n- CGクリエイター専攻\n\nデザイン・イラストワールドには２つの専攻がある。\n\n- クリエイティブデザイン専攻\n- デジタルイラスト専攻\n\n自分らしさを活かし「創造力」を仕事に！「産学連携」を活かした独自の教育システム\n\n京都TECHでは、技術・コミュニケーションそして3つの考え方を学ぶ。\n\n### CREATIVITY\n\n無限の創造力を発揮することの大切さ。\n\n### INNOVATION\n\n変化の時代に常に新しい考えを生み出すことの大切さ。\n\n### LEADERSHIP\n\n世界中の人々に共感を与え、感動と行動を生み出す大切さ。\n\n京都TECHは、「自分らしさ」を活かし、未来をつくる人材を育成します。\n\n**京都TECH独自の教育システム**\n\n京都TECHにはあなたをIT・デザイン業界の成功へと導く確かなシナリオがあります。入学前からあなたの夢や目標に向かってスタートするあなたの為のMyスクールや、\n 業界のプロと共に行う企業プロジェクトや企業課題、業界のトッププロからの特別講義、 \nそして日々のカリキュラム等在学中から業界のプロと共に学ぶ事により、より高いレベルでの就職・デビューを目指せます。\n学食はありません。"},{"role":"user","content":data}],
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None)

            #print("あなた :"+ data)
            text=response['choices'][0]['message']['content']
            #print("AI :"+ text)

            #しゃべらす
            # Note: the voice setting will not overwrite the voice element in input SSML.
            speech_config.speech_synthesis_voice_name = "ja-JP-NanamiNeural"

            # use the default speaker as audio output.
            speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

            result = speech_synthesizer.speak_text_async(text).get()
            # Check result
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print("Speech synthesized for text [{}]".format(text))
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print("Speech synthesis canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(cancellation_details.error_details))

    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("音声が認識できませんでした: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("音声認識がキャンセルされました: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("エラーの詳細: {}".format(cancellation_details.error_details))
            print("Speechリソースのキーとリージョンの値を設定しましたか？")
    speech_recognize_keyword_locally_from_microphone()

def speech_recognize_keyword_locally_from_microphone():
    """ローカルでキーワードの検出を実行し、結果のオーディオに直接アクセスします"""

    # キーワード認識モデルのインスタンスを作成します。使用するキーワード認識モデルの場所に更新してください。
    model = speechsdk.KeywordRecognitionModel(table)

    # キーワード認識モデルがトリガーとするフレーズです。
    keyword = Hey

    # 入力にはデフォルトのマイクデバイスを使用してローカルのキーワード認識器を作成します。
    keyword_recognizer = speechsdk.KeywordRecognizer()

    done = False

    def recognized_cb(evt):
        # キーワードフレーズのみが認識されます。結果は 'NoMatch' ではなく、タイムアウトもありません。
        # キーワードフレーズが検出されるか、認識がキャンセルされる（stop_recognition_async() によるもの、
        # 入力ファイルやストリームの終了によるもの）まで、認識器が実行されます。
        result = evt.result
        if result.reason == speechsdk.ResultReason.RecognizedKeyword:
            print("キーワードが認識されました: {}".format(result.text))
        nonlocal done
        done = True

    def canceled_cb(evt):
        result = evt.result
        if result.reason == speechsdk.ResultReason.Canceled:
            print('キャンセルされました: {}'.format(result.cancellation_details.reason))
        nonlocal done
        done = True

    # キーワード認識器が発生するイベントにコールバックを接続します。
    keyword_recognizer.recognized.connect(recognized_cb)
    keyword_recognizer.canceled.connect(canceled_cb)

    # キーワード検出を開始します。
    result_future = keyword_recognizer.recognize_once_async(model)
    print('キーワード "{}" で始まるフレーズを話し、その後に何でも話してください...'.format(keyword))
    result = result_future.get()

    if result.reason == speechsdk.ResultReason.RecognizedKeyword:
        recognize_from_microphone()  # 音声認識を開始

    # 結果が出る前にアクティブなキーワード検出を停止する必要がある場合は、以下の方法で行うことができます。
    #
    #   stop_future = keyword_recognizer.stop_recognition_async()
    #   print('停止中...')
    #   stopped = stop_future.get()

# 関数の呼び出し
speech_recognize_keyword_locally_from_microphone()
