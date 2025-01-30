#Jugend forscht Wolfserkennung
##1. Idee
Ich war schon immer ein Tierfreund und als ich wiederholt Artikel im 
Stader Tageblatt gelesen habe, dass Wölfe, die Weidetiere wie Schafe 
oder Rinder reißen, zum Abschuss freigegeben werden, entstand die 
Idee zu meinem Projekt. Eine Zusammenarbeit mit der Wolfsberaterin 
Svenja Oßenbrügge ergab, dass ein KI unterstütztes Kamerasystem 
sehr wichtig für das Wolfsmonitoring wäre, da die Hälfte der Wolfsrisse 
mutmaßlich auf Hunde zurückzuführen sind. Eindeutige Bilder sorgen 
für Aufklärung und mein entwickeltes Alarmsystem kann Tiere schützen.
##2. Ziel
•Das neuronale Netzwerk aus dem Vorjahr verbessern und so 
anpassen, dass es sowohl Hunde als auch Wölfe erkennen kann 
•Das neuronale Netzwerk mit dem Raspberry Pi verbinden
•Die Kamera aus dem Vorjahr verbessern
•Eine Möglichkeit einbauen, dass der Raspberry Pi unabhängig von 
WLAN-Netzwerken eine SMS senden kann
•Alles in einer funktionalen Kamerabox verbinden, die, wenn sie eine 
Bewegung erkennt, ein Video aufnimmt, dieses klassifiziert und zuletzt 
gegebenenfalls eine SMS-Nachricht an den Verantwortlichen sendet

##3. Vorgehensweise
###3.1 Wie bin ich vorgegangen?
•Trainingsdaten mit Roboflow vorbereitet
•Mit YOLOv8 ein Modell erstellt
•Modell auf Google Colab trainiert
•Modell in das .hef-Format konvertiert
•Python Programm geschrieben, welches auf dem Raspberry Pi läuft 
und bei einer Bewegung den Kamera-Stream mit der Klassifizierung 
öffnet 
###3.2 Problemlösemethoden bei der                     
KI-Entwicklung
Problem aufgetreten → Hypothese aufstellen → Versuch entwickeln →
erneut testen → ggf. einsatzbereit machen oder weitere Lösungen 
entwickeln
###3.3 Verwendete Hardware
####3.3.1 Raspberry Pi
Der Raspberry Pi ist ein Minicomputer. Auf diesem läuft das Python-
Programm, welches sozusagen alles koordiniert.
####3.3.2 Raspberry Pi Kamera v3
Um die Bilder, bzw. Videos aufzunehmen, verwende ich die Raspberry 
Pi Kamera v3. Diese hat im Gegensatz zu meiner vorherigen Kamera 
einen Autofokus und hat keinen Infrarotfilter, sodass ich einen Infrarot-
Scheinwerfer verwenden kann.
####3.3.3 SIM-Hat
Um eine SMS an den Verantwortlichen zu senden, verwende ich den 
Waveshare SIM7600E-H 4g HAT. Mit diesem kann ich unabhängig von 
WLAN-Netzwerken SMS-Nachrichten versenden.
####3.3.4 Infrarot-LED
Damit meine Kamera auch in der Nacht sehen kann, verwende ich eine 
Infrarot-LED, da meine Kamera keinen Infrarot Filter hat und somit 
keine anderen Tiere durch das Licht gestört werden.
####3.3.5 AI-HAT
Da mein vorheriges System ca. 20-30 Sekunden brauchte, um ein Bild 
zu verarbeiten, verwende ich den Raspberry Pi AI HAT. Dieser hat 13 
TOPS und ich kann mit ihm einen 30fps Videostream meiner Kamera 
live verarbeiten, womit mein System nun echtzeitfähig ist. Dieses hat 
den Vorteil, dass durch die höhere Verarbeitungsgeschwindigkeit mehr 
Frames analysiert und erkannt werden können. Dieses sichert und 
erhöht die Qualität der Wolfserkennung und führt schneller zu einem 
Alarm, da ein Verarbeitungsrückstau an einzeln aufgenommen Fotos 
vermieden wird.

##4. Tests
###4.1 Vorversuch mit meiner Katze
Am Beispiel meiner Katze wurden viele Funktionalitäten meines Systems 
entwickelt und getestet. 
###4.2 Hund
Um zu erkennen, ob die Kamera relevante Tiere erkennt, habe ich dies 
zunächst an Hunden ausprobiert. Da ich selbst keinen Hund habe, testete 
ich dies an Hunden von Freunden, bzw. Bekannten. Dies habe ich sowohl 
mit einem Videostream als auch mit einzelnen Bildern gemacht. Die Hunde 
wurden fast immer erkannt. Wenn sie nicht erkannt wurden, lag dies meist 
daran, dass sich der Hund sehr weit hinten im Bild befand.
###4.3 Wolf
Um auszuprobieren, ob meine KI auch mit echten Wölfen funktioniert und 
nicht nur mit Hunden, bin ich in den Wildpark Schwarze Berge gefahren, 
um dort meine Kamera an den Wölfen auszuprobieren. Vor Ort hat mir die 
Wolfsberaterin Svenja Oßenbrügge geholfen, indem sie die Wölfe 
angelockt hat, da das Gehege sehr groß ist. Die Genauigkeit meiner KI bei 
diesem Versuch war sehr zufriedenstellend. Die Wölfe wurden im 
Gegensatz zum letzten Wildparkbesuch fast immer erkannt. Die so 
ziemlich einzige Ausnahme war, wenn der Wolf flach auf dem Boden lag. 
Dies liegt höchstwahrscheinlich daran, dass es wenig Bilder von liegenden 
Wölfen im meinen Trainingsbildern gab.

##5. Was ist neu?
• Raspberry Pi
• AI HAT
• SIM-HAT
• Raspberry Pi Kamera
• Neuronales Netzwerk
• Infrarot LED
• Python-Programm
• 3D-Gedrucke Box

##6. Zielerreichung
• Ich habe das neuronale Netzwerk mit YOLOv8 verbessert
• Das neuronale Netzwerk kann nun Hunde und Wölfe erkennen, was entscheidend für die Verbesserung des Wolfsmonitorings ist
• Ich habe nun eine Kamera mit Autofokus
• Mein Raspberry Pi hat nun einen SIM-HAT und somit die Möglichkeit SMS-Nachrichten an einen Verantwortlichen zu verschicken
• Ich habe alles in einer funktionalen Kamerabox verbunden

##7. Ergebnisdiskussion
Mein Kamerasystem soll Tierhalter wie Schafhirten vor angreifenden 
Hunden oder Wölfen warnen, damit sie rechtzeitig reagieren und ihre Tiere 
schützen können. Außerdem soll es Wolfberatern, bei Wildrissen helfen 
zwischen Hund und Wolf zu unterscheiden und wichtige Erkenntnisse über 
das Verhalten von Wölfen liefern. Derzeit fehlen oft Bild- oder 
Videobeweise bei Wolfsrissen, sodass Entscheidungen nur auf DNA-
Proben und Angriffsweisen basieren. Videoaufnahmen könnten 
Fehleinschätzungen minimieren und das Wolfsmonitoring verbessern. Ich 
habe alle Systemkomponenten erfolgreich getestet: Der Bewegungsmelder 
funktionierte mit meiner Katze, und die KI erkannte zuverlässig Hunde und 
Wölfe, was ich erfolgreich mit echten Tieren bestätigen konnte. Mein 
System ist nun echtzeitfähig und einsatzbereit, Tag und Nacht tauglich, 
wetterfest und internetfähig. Dadurch sollten in Zukunft eine 
Zusammenarbeit mit kompetenten Partnern angestrebt werden, zum 
Beispiel Schäfer, Jäger, Wolfsberater, Verhaltensforscher, Ranger, 
Wildhüter, …

##8. Danksagung
An dieser Stelle möchte ich mich bei all denjenigen bedanken, die mich bei 
meinem Projekt unterstützt und motiviert haben. Zuerst gebührt mein Dank 
Herrn Privatdozent Dr. Carmesin, der mein Projekt betreut und mir bei der 
Organisation des Projektes geholfen hat. Ein besonderer Dank gilt Frau 
von Bargen, die mir mit viel Geduld, Interesse und Hilfsbereitschaft 
insbesondere beim Schreiben der Langfassung zur Seite stand. Ich 
möchte mich außerdem bei Svenja Oßenbrügge, Wolfsberaterin Landkreis 
Hamburg-Harburg, und dem Wildpark Schwarze Berge für die 
vertiefenden, weiterführenden Informationen zum Riss von Weide- und 
Nutztieren und für die Unterstützung bei der Wolfsbeobachtung am 
Wolfsgehege des Wildparks Schwarze Berge bedanken. Ich möchte mich 
außerdem bei Jannes Ruder für das 3D-Modelling und Drucken meiner 
Box bedanken. Zu guter Letzt möchte ich mich bei Florian von Bargen und 
meiner Familie bedanken, die stets ein offenes Ohr für mich hatten. 


