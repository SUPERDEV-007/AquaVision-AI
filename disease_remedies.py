"""
Disease Remedies Database with Multi-language Support
"""

# Disease information and remedies in multiple languages
DISEASE_INFO = {
    "Aeromoniasis": {
        "english": {
            "name": "Aeromoniasis",
            "type": "Bacterial Disease",
            "symptoms": [
                "Red spots or ulcers on the body",
                "Fin rot",
                "Swollen abdomen",
                "Loss of appetite",
                "Lethargy"
            ],
            "causes": [
                "Poor water quality",
                "Stress",
                "Overcrowding",
                "Injuries"
            ],
            "remedies": [
                "Improve water quality - change 25-30% water daily",
                "Add salt (1-2 teaspoons per gallon) to reduce stress",
                "Use antibiotics: Oxytetracycline or Kanamycin",
                "Isolate infected fish",
                "Maintain water temperature at 24-26°C",
                "Increase aeration"
            ],
            "prevention": [
                "Maintain clean water with regular changes",
                "Avoid overcrowding",
                "Quarantine new fish",
                "Feed high-quality food"
            ]
        },
        "hindi": {
            "name": "एरोमोनियासिस",
            "type": "जीवाणु रोग",
            "symptoms": [
                "शरीर पर लाल धब्बे या अल्सर",
                "पंख सड़ना",
                "सूजा हुआ पेट",
                "भूख न लगना",
                "सुस्ती"
            ],
            "causes": [
                "खराब पानी की गुणवत्ता",
                "तनाव",
                "भीड़-भाड़",
                "चोटें"
            ],
            "remedies": [
                "पानी की गुणवत्ता में सुधार - प्रतिदिन 25-30% पानी बदलें",
                "तनाव कम करने के लिए नमक मिलाएं (प्रति गैलन 1-2 चम्मच)",
                "एंटीबायोटिक्स का उपयोग करें: ऑक्सीटेट्रासाइक्लिन या कनामाइसिन",
                "संक्रमित मछली को अलग करें",
                "पानी का तापमान 24-26°C पर बनाए रखें",
                "वातन बढ़ाएं"
            ],
            "prevention": [
                "नियमित बदलाव के साथ साफ पानी बनाए रखें",
                "भीड़-भाड़ से बचें",
                "नई मछलियों को क्वारंटाइन करें",
                "उच्च गुणवत्ता वाला भोजन दें"
            ]
        },
        "kannada": {
            "name": "ಏರೋಮೋನಿಯಾಸಿಸ್",
            "type": "ಬ್ಯಾಕ್ಟೀರಿಯಾದ ರೋಗ",
            "symptoms": [
                "ದೇಹದ ಮೇಲೆ ಕೆಂಪು ಚುಕ್ಕೆಗಳು ಅಥವಾ ಹುಣ್ಣುಗಳು",
                "ರೆಕ್ಕೆ ಕೊಳೆತ",
                "ಉಬ್ಬಿದ ಹೊಟ್ಟೆ",
                "ಹಸಿವು ಕಡಿಮೆ",
                "ಸೋಮಾರಿತನ"
            ],
            "causes": [
                "ಕಳಪೆ ನೀರಿನ ಗುಣಮಟ್ಟ",
                "ಒತ್ತಡ",
                "ಅತಿಯಾದ ಸಂಖ್ಯೆ",
                "ಗಾಯಗಳು"
            ],
            "remedies": [
                "ನೀರಿನ ಗುಣಮಟ್ಟವನ್ನು ಸುಧಾರಿಸಿ - ದೈನಂದಿನ 25-30% ನೀರನ್ನು ಬದಲಾಯಿಸಿ",
                "ಒತ್ತಡವನ್ನು ಕಡಿಮೆ ಮಾಡಲು ಉಪ್ಪು ಸೇರಿಸಿ (ಪ್ರತಿ ಗ್ಯಾಲನ್ಗೆ 1-2 ಚಮಚ)",
                "ಆಂಟಿಬಯೋಟಿಕ್ಗಳನ್ನು ಬಳಸಿ: ಆಕ್ಸಿಟೆಟ್ರಾಸೈಕ್ಲಿನ್ ಅಥವಾ ಕನಾಮೈಸಿನ್",
                "ಸೋಂಕಿತ ಮೀನುಗಳನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ",
                "ನೀರಿನ ತಾಪಮಾನವನ್ನು 24-26°C ನಲ್ಲಿ ನಿರ್ವಹಿಸಿ",
                "ವಾಯುಚಲನೆಯನ್ನು ಹೆಚ್ಚಿಸಿ"
            ],
            "prevention": [
                "ನಿಯಮಿತ ಬದಲಾವಣೆಗಳೊಂದಿಗೆ ಸ್ವಚ್ಛ ನೀರನ್ನು ನಿರ್ವಹಿಸಿ",
                "ಅತಿಯಾದ ಸಂಖ್ಯೆಯನ್ನು ತಪ್ಪಿಸಿ",
                "ಹೊಸ ಮೀನುಗಳನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ",
                "ಉನ್ನತ ಗುಣಮಟ್ಟದ ಆಹಾರವನ್ನು ನೀಡಿ"
            ]
        }
    },
    "Gill Disease": {
        "english": {
            "name": "Gill Disease",
            "type": "Bacterial Disease",
            "symptoms": [
                "Rapid gill movement",
                "Gasping at water surface",
                "Red or swollen gills",
                "Loss of appetite",
                "Lethargy"
            ],
            "causes": [
                "Poor water quality",
                "High ammonia levels",
                "Bacterial infection",
                "Parasites"
            ],
            "remedies": [
                "Immediate water change (50%)",
                "Add aquarium salt (1 teaspoon per gallon)",
                "Use antibiotics: Tetracycline or Erythromycin",
                "Increase aeration and oxygen",
                "Reduce feeding",
                "Maintain pH between 6.5-7.5"
            ],
            "prevention": [
                "Regular water testing",
                "Maintain proper filtration",
                "Avoid overfeeding",
                "Quarantine new fish"
            ]
        },
        "hindi": {
            "name": "गिल रोग",
            "type": "जीवाणु रोग",
            "symptoms": [
                "तेज गिल हिलना",
                "पानी की सतह पर हांफना",
                "लाल या सूजे हुए गिल",
                "भूख न लगना",
                "सुस्ती"
            ],
            "causes": [
                "खराब पानी की गुणवत्ता",
                "उच्च अमोनिया स्तर",
                "जीवाणु संक्रमण",
                "परजीवी"
            ],
            "remedies": [
                "तुरंत पानी बदलें (50%)",
                "एक्वेरियम नमक मिलाएं (प्रति गैलन 1 चम्मच)",
                "एंटीबायोटिक्स का उपयोग करें: टेट्रासाइक्लिन या एरिथ्रोमाइसिन",
                "वातन और ऑक्सीजन बढ़ाएं",
                "भोजन कम करें",
                "pH को 6.5-7.5 के बीच बनाए रखें"
            ],
            "prevention": [
                "नियमित पानी की जांच",
                "उचित निस्पंदन बनाए रखें",
                "अधिक भोजन देने से बचें",
                "नई मछलियों को क्वारंटाइन करें"
            ]
        },
        "kannada": {
            "name": "ಗಿಲ್ ರೋಗ",
            "type": "ಬ್ಯಾಕ್ಟೀರಿಯಾದ ರೋಗ",
            "symptoms": [
                "ವೇಗವಾದ ಗಿಲ್ ಚಲನೆ",
                "ನೀರಿನ ಮೇಲ್ಮೈಯಲ್ಲಿ ಉಸಿರಾಡುವುದು",
                "ಕೆಂಪು ಅಥವಾ ಉಬ್ಬಿದ ಗಿಲ್ಗಳು",
                "ಹಸಿವು ಕಡಿಮೆ",
                "ಸೋಮಾರಿತನ"
            ],
            "causes": [
                "ಕಳಪೆ ನೀರಿನ ಗುಣಮಟ್ಟ",
                "ಅಧಿಕ ಅಮೋನಿಯಾ ಮಟ್ಟ",
                "ಬ್ಯಾಕ್ಟೀರಿಯಾದ ಸೋಂಕು",
                "ಪರಾವಲಂಬಿಗಳು"
            ],
            "remedies": [
                "ತಕ್ಷಣ ನೀರನ್ನು ಬದಲಾಯಿಸಿ (50%)",
                "ಅಕ್ವೇರಿಯಂ ಉಪ್ಪು ಸೇರಿಸಿ (ಪ್ರತಿ ಗ್ಯಾಲನ್ಗೆ 1 ಚಮಚ)",
                "ಆಂಟಿಬಯೋಟಿಕ್ಗಳನ್ನು ಬಳಸಿ: ಟೆಟ್ರಾಸೈಕ್ಲಿನ್ ಅಥವಾ ಎರಿಥ್ರೋಮೈಸಿನ್",
                "ವಾಯುಚಲನೆ ಮತ್ತು ಆಮ್ಲಜನಕವನ್ನು ಹೆಚ್ಚಿಸಿ",
                "ಆಹಾರವನ್ನು ಕಡಿಮೆ ಮಾಡಿ",
                "pH ಅನ್ನು 6.5-7.5 ನಡುವೆ ನಿರ್ವಹಿಸಿ"
            ],
            "prevention": [
                "ನಿಯಮಿತ ನೀರಿನ ಪರೀಕ್ಷೆ",
                "ಸರಿಯಾದ ಫಿಲ್ಟರೇಶನ್ ನಿರ್ವಹಿಸಿ",
                "ಅತಿಯಾದ ಆಹಾರ ನೀಡುವುದನ್ನು ತಪ್ಪಿಸಿ",
                "ಹೊಸ ಮೀನುಗಳನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ"
            ]
        }
    },
    "Healthy": {
        "english": {
            "name": "Healthy Fish",
            "type": "Normal Condition",
            "symptoms": [
                "Active swimming",
                "Good appetite",
                "Bright colors",
                "Clear eyes",
                "Normal breathing"
            ],
            "causes": [
                "Proper care",
                "Good water quality",
                "Balanced diet"
            ],
            "remedies": [
                "Continue current care routine",
                "Maintain water quality",
                "Provide balanced nutrition",
                "Regular health monitoring"
            ],
            "prevention": [
                "Regular water changes",
                "Proper feeding schedule",
                "Monitor water parameters",
                "Quarantine new additions"
            ]
        },
        "hindi": {
            "name": "स्वस्थ मछली",
            "type": "सामान्य स्थिति",
            "symptoms": [
                "सक्रिय तैराकी",
                "अच्छी भूख",
                "चमकीले रंग",
                "स्पष्ट आंखें",
                "सामान्य सांस लेना"
            ],
            "causes": [
                "उचित देखभाल",
                "अच्छी पानी की गुणवत्ता",
                "संतुलित आहार"
            ],
            "remedies": [
                "वर्तमान देखभाल दिनचर्या जारी रखें",
                "पानी की गुणवत्ता बनाए रखें",
                "संतुलित पोषण प्रदान करें",
                "नियमित स्वास्थ्य निगरानी"
            ],
            "prevention": [
                "नियमित पानी बदलना",
                "उचित भोजन अनुसूची",
                "पानी के मापदंडों की निगरानी",
                "नए जोड़ों को क्वारंटाइन करें"
            ]
        },
        "kannada": {
            "name": "ಆರೋಗ್ಯಕರ ಮೀನು",
            "type": "ಸಾಮಾನ್ಯ ಸ್ಥಿತಿ",
            "symptoms": [
                "ಸಕ್ರಿಯ ಈಜುವಿಕೆ",
                "ಉತ್ತಮ ಹಸಿವು",
                "ಪ್ರಕಾಶಮಾನವಾದ ಬಣ್ಣಗಳು",
                "ಸ್ಪಷ್ಟ ಕಣ್ಣುಗಳು",
                "ಸಾಮಾನ್ಯ ಉಸಿರಾಟ"
            ],
            "causes": [
                "ಸರಿಯಾದ ಕಾಳಜಿ",
                "ಉತ್ತಮ ನೀರಿನ ಗುಣಮಟ್ಟ",
                "ಸಮತೋಲಿತ ಆಹಾರ"
            ],
            "remedies": [
                "ಪ್ರಸ್ತುತ ಕಾಳಜಿ ನಿಯಮವನ್ನು ಮುಂದುವರಿಸಿ",
                "ನೀರಿನ ಗುಣಮಟ್ಟವನ್ನು ನಿರ್ವಹಿಸಿ",
                "ಸಮತೋಲಿತ ಪೋಷಣೆಯನ್ನು ನೀಡಿ",
                "ನಿಯಮಿತ ಆರೋಗ್ಯ ಮೇಲ್ವಿಚಾರಣೆ"
            ],
            "prevention": [
                "ನಿಯಮಿತ ನೀರಿನ ಬದಲಾವಣೆಗಳು",
                "ಸರಿಯಾದ ಆಹಾರ ವೇಳಾಪಟ್ಟಿ",
                "ನೀರಿನ ನಿಯತಾಂಕಗಳನ್ನು ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಿ",
                "ಹೊಸ ಸೇರ್ಪಡೆಗಳನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ"
            ]
        }
    },
    "Parasitic Disease": {
        "english": {
            "name": "Parasitic Disease",
            "type": "Parasitic Infection",
            "symptoms": [
                "Flashing (rubbing against objects)",
                "White spots on body",
                "Excessive mucus",
                "Rapid breathing",
                "Loss of appetite"
            ],
            "causes": [
                "Parasite infestation",
                "Poor water quality",
                "Stress",
                "New fish introduction"
            ],
            "remedies": [
                "Use anti-parasitic medication: Malachite Green or Formalin",
                "Increase water temperature to 28-30°C",
                "Add salt (1-2 teaspoons per gallon)",
                "Improve water quality",
                "Isolate infected fish",
                "Treat entire tank if needed"
            ],
            "prevention": [
                "Quarantine new fish for 2-3 weeks",
                "Maintain good water quality",
                "Avoid overcrowding",
                "Regular health checks"
            ]
        },
        "hindi": {
            "name": "परजीवी रोग",
            "type": "परजीवी संक्रमण",
            "symptoms": [
                "चमकना (वस्तुओं के खिलाफ रगड़ना)",
                "शरीर पर सफेद धब्बे",
                "अत्यधिक बलगम",
                "तेज सांस लेना",
                "भूख न लगना"
            ],
            "causes": [
                "परजीवी संक्रमण",
                "खराब पानी की गुणवत्ता",
                "तनाव",
                "नई मछली का परिचय"
            ],
            "remedies": [
                "एंटी-परजीवी दवा का उपयोग करें: मैलाकाइट ग्रीन या फॉर्मलिन",
                "पानी का तापमान 28-30°C तक बढ़ाएं",
                "नमक मिलाएं (प्रति गैलन 1-2 चम्मच)",
                "पानी की गुणवत्ता में सुधार करें",
                "संक्रमित मछली को अलग करें",
                "आवश्यकता होने पर पूरे टैंक का इलाज करें"
            ],
            "prevention": [
                "नई मछलियों को 2-3 सप्ताह के लिए क्वारंटाइन करें",
                "अच्छी पानी की गुणवत्ता बनाए रखें",
                "भीड़-भाड़ से बचें",
                "नियमित स्वास्थ्य जांच"
            ]
        },
        "kannada": {
            "name": "ಪರಾವಲಂಬಿ ರೋಗ",
            "type": "ಪರಾವಲಂಬಿ ಸೋಂಕು",
            "symptoms": [
                "ಹೊಳಪು (ವಸ್ತುಗಳ ವಿರುದ್ಧ ಉಜ್ಜುವುದು)",
                "ದೇಹದ ಮೇಲೆ ಬಿಳಿ ಚುಕ್ಕೆಗಳು",
                "ಅತಿಯಾದ ಲೋಳೆ",
                "ವೇಗವಾದ ಉಸಿರಾಟ",
                "ಹಸಿವು ಕಡಿಮೆ"
            ],
            "causes": [
                "ಪರಾವಲಂಬಿ ಸೋಂಕು",
                "ಕಳಪೆ ನೀರಿನ ಗುಣಮಟ್ಟ",
                "ಒತ್ತಡ",
                "ಹೊಸ ಮೀನು ಪರಿಚಯ"
            ],
            "remedies": [
                "ಆಂಟಿ-ಪರಾವಲಂಬಿ ಔಷಧವನ್ನು ಬಳಸಿ: ಮ್ಯಾಲಾಕೈಟ್ ಗ್ರೀನ್ ಅಥವಾ ಫಾರ್ಮಲಿನ್",
                "ನೀರಿನ ತಾಪಮಾನವನ್ನು 28-30°C ಗೆ ಹೆಚ್ಚಿಸಿ",
                "ಉಪ್ಪು ಸೇರಿಸಿ (ಪ್ರತಿ ಗ್ಯಾಲನ್ಗೆ 1-2 ಚಮಚ)",
                "ನೀರಿನ ಗುಣಮಟ್ಟವನ್ನು ಸುಧಾರಿಸಿ",
                "ಸೋಂಕಿತ ಮೀನುಗಳನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ",
                "ಅಗತ್ಯವಿದ್ದರೆ ಸಂಪೂರ್ಣ ಟ್ಯಾಂಕ್ ಅನ್ನು ಚಿಕಿತ್ಸೆ ಮಾಡಿ"
            ],
            "prevention": [
                "ಹೊಸ ಮೀನುಗಳನ್ನು 2-3 ವಾರಗಳ ಕಾಲ ಪ್ರತ್ಯೇಕಿಸಿ",
                "ಉತ್ತಮ ನೀರಿನ ಗುಣಮಟ್ಟವನ್ನು ನಿರ್ವಹಿಸಿ",
                "ಅತಿಯಾದ ಸಂಖ್ಯೆಯನ್ನು ತಪ್ಪಿಸಿ",
                "ನಿಯಮಿತ ಆರೋಗ್ಯ ಪರೀಕ್ಷೆಗಳು"
            ]
        }
    },
    "Red Disease": {
        "english": {
            "name": "Red Disease",
            "type": "Bacterial Disease",
            "symptoms": [
                "Red patches or streaks on body",
                "Fin rot",
                "Ulcers",
                "Loss of appetite",
                "Lethargy"
            ],
            "causes": [
                "Bacterial infection (Aeromonas)",
                "Poor water quality",
                "Stress",
                "Injuries"
            ],
            "remedies": [
                "Use antibiotics: Oxytetracycline or Kanamycin",
                "Improve water quality - change 30% daily",
                "Add salt (1-2 teaspoons per gallon)",
                "Isolate infected fish",
                "Maintain water temperature at 24-26°C",
                "Increase aeration"
            ],
            "prevention": [
                "Maintain clean water",
                "Avoid overcrowding",
                "Handle fish carefully",
                "Quarantine new fish"
            ]
        },
        "hindi": {
            "name": "लाल रोग",
            "type": "जीवाणु रोग",
            "symptoms": [
                "शरीर पर लाल धब्बे या धारियां",
                "पंख सड़ना",
                "अल्सर",
                "भूख न लगना",
                "सुस्ती"
            ],
            "causes": [
                "जीवाणु संक्रमण (एरोमोनास)",
                "खराब पानी की गुणवत्ता",
                "तनाव",
                "चोटें"
            ],
            "remedies": [
                "एंटीबायोटिक्स का उपयोग करें: ऑक्सीटेट्रासाइक्लिन या कनामाइसिन",
                "पानी की गुणवत्ता में सुधार - प्रतिदिन 30% बदलें",
                "नमक मिलाएं (प्रति गैलन 1-2 चम्मच)",
                "संक्रमित मछली को अलग करें",
                "पानी का तापमान 24-26°C पर बनाए रखें",
                "वातन बढ़ाएं"
            ],
            "prevention": [
                "साफ पानी बनाए रखें",
                "भीड़-भाड़ से बचें",
                "मछली को सावधानी से संभालें",
                "नई मछलियों को क्वारंटाइन करें"
            ]
        },
        "kannada": {
            "name": "ಕೆಂಪು ರೋಗ",
            "type": "ಬ್ಯಾಕ್ಟೀರಿಯಾದ ರೋಗ",
            "symptoms": [
                "ದೇಹದ ಮೇಲೆ ಕೆಂಪು ಪ್ಯಾಚ್ಗಳು ಅಥವಾ ಗೆರೆಗಳು",
                "ರೆಕ್ಕೆ ಕೊಳೆತ",
                "ಹುಣ್ಣುಗಳು",
                "ಹಸಿವು ಕಡಿಮೆ",
                "ಸೋಮಾರಿತನ"
            ],
            "causes": [
                "ಬ್ಯಾಕ್ಟೀರಿಯಾದ ಸೋಂಕು (ಏರೋಮೋನಾಸ್)",
                "ಕಳಪೆ ನೀರಿನ ಗುಣಮಟ್ಟ",
                "ಒತ್ತಡ",
                "ಗಾಯಗಳು"
            ],
            "remedies": [
                "ಆಂಟಿಬಯೋಟಿಕ್ಗಳನ್ನು ಬಳಸಿ: ಆಕ್ಸಿಟೆಟ್ರಾಸೈಕ್ಲಿನ್ ಅಥವಾ ಕನಾಮೈಸಿನ್",
                "ನೀರಿನ ಗುಣಮಟ್ಟವನ್ನು ಸುಧಾರಿಸಿ - ದೈನಂದಿನ 30% ಬದಲಾಯಿಸಿ",
                "ಉಪ್ಪು ಸೇರಿಸಿ (ಪ್ರತಿ ಗ್ಯಾಲನ್ಗೆ 1-2 ಚಮಚ)",
                "ಸೋಂಕಿತ ಮೀನುಗಳನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ",
                "ನೀರಿನ ತಾಪಮಾನವನ್ನು 24-26°C ನಲ್ಲಿ ನಿರ್ವಹಿಸಿ",
                "ವಾಯುಚಲನೆಯನ್ನು ಹೆಚ್ಚಿಸಿ"
            ],
            "prevention": [
                "ಸ್ವಚ್ಛ ನೀರನ್ನು ನಿರ್ವಹಿಸಿ",
                "ಅತಿಯಾದ ಸಂಖ್ಯೆಯನ್ನು ತಪ್ಪಿಸಿ",
                "ಮೀನುಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ನಿರ್ವಹಿಸಿ",
                "ಹೊಸ ಮೀನುಗಳನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ"
            ]
        }
    },
    "Saprolegniasis": {
        "english": {
            "name": "Saprolegniasis",
            "type": "Fungal Disease",
            "symptoms": [
                "White cotton-like growth on body",
                "Fuzzy patches",
                "Loss of appetite",
                "Lethargy",
                "Fin rot"
            ],
            "causes": [
                "Fungal infection",
                "Poor water quality",
                "Injuries",
                "Stress"
            ],
            "remedies": [
                "Use antifungal medication: Methylene Blue or Malachite Green",
                "Improve water quality",
                "Add salt (1-2 teaspoons per gallon)",
                "Increase water temperature to 26-28°C",
                "Isolate infected fish",
                "Remove dead tissue if possible"
            ],
            "prevention": [
                "Maintain clean water",
                "Avoid injuries",
                "Reduce stress",
                "Proper nutrition"
            ]
        },
        "hindi": {
            "name": "सैप्रोलेग्नियासिस",
            "type": "फंगल रोग",
            "symptoms": [
                "शरीर पर सफेद रूई जैसी वृद्धि",
                "फजी धब्बे",
                "भूख न लगना",
                "सुस्ती",
                "पंख सड़ना"
            ],
            "causes": [
                "फंगल संक्रमण",
                "खराब पानी की गुणवत्ता",
                "चोटें",
                "तनाव"
            ],
            "remedies": [
                "एंटीफंगल दवा का उपयोग करें: मिथाइलीन ब्लू या मैलाकाइट ग्रीन",
                "पानी की गुणवत्ता में सुधार करें",
                "नमक मिलाएं (प्रति गैलन 1-2 चम्मच)",
                "पानी का तापमान 26-28°C तक बढ़ाएं",
                "संक्रमित मछली को अलग करें",
                "यदि संभव हो तो मृत ऊतक को हटाएं"
            ],
            "prevention": [
                "साफ पानी बनाए रखें",
                "चोटों से बचें",
                "तनाव कम करें",
                "उचित पोषण"
            ]
        },
        "kannada": {
            "name": "ಸ್ಯಾಪ್ರೋಲೆಗ್ನಿಯಾಸಿಸ್",
            "type": "ಫಂಗಲ್ ರೋಗ",
            "symptoms": [
                "ದೇಹದ ಮೇಲೆ ಬಿಳಿ ಹತ್ತಿ ತರಹದ ಬೆಳವಣಿಗೆ",
                "ನಯವಾದ ಪ್ಯಾಚ್ಗಳು",
                "ಹಸಿವು ಕಡಿಮೆ",
                "ಸೋಮಾರಿತನ",
                "ರೆಕ್ಕೆ ಕೊಳೆತ"
            ],
            "causes": [
                "ಫಂಗಲ್ ಸೋಂಕು",
                "ಕಳಪೆ ನೀರಿನ ಗುಣಮಟ್ಟ",
                "ಗಾಯಗಳು",
                "ಒತ್ತಡ"
            ],
            "remedies": [
                "ಆಂಟಿಫಂಗಲ್ ಔಷಧವನ್ನು ಬಳಸಿ: ಮೆಥಿಲೀನ್ ಬ್ಲೂ ಅಥವಾ ಮ್ಯಾಲಾಕೈಟ್ ಗ್ರೀನ್",
                "ನೀರಿನ ಗುಣಮಟ್ಟವನ್ನು ಸುಧಾರಿಸಿ",
                "ಉಪ್ಪು ಸೇರಿಸಿ (ಪ್ರತಿ ಗ್ಯಾಲನ್ಗೆ 1-2 ಚಮಚ)",
                "ನೀರಿನ ತಾಪಮಾನವನ್ನು 26-28°C ಗೆ ಹೆಚ್ಚಿಸಿ",
                "ಸೋಂಕಿತ ಮೀನುಗಳನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ",
                "ಸಾಧ್ಯವಾದರೆ ಸತ್ತ ಊತಕವನ್ನು ತೆಗೆದುಹಾಕಿ"
            ],
            "prevention": [
                "ಸ್ವಚ್ಛ ನೀರನ್ನು ನಿರ್ವಹಿಸಿ",
                "ಗಾಯಗಳನ್ನು ತಪ್ಪಿಸಿ",
                "ಒತ್ತಡವನ್ನು ಕಡಿಮೆ ಮಾಡಿ",
                "ಸರಿಯಾದ ಪೋಷಣೆ"
            ]
        }
    },
    "White Tail Disease": {
        "english": {
            "name": "White Tail Disease",
            "type": "Viral Disease",
            "symptoms": [
                "White discoloration of tail",
                "Tail rot",
                "Loss of tail fin",
                "Lethargy",
                "Loss of appetite"
            ],
            "causes": [
                "Viral infection",
                "Poor water quality",
                "Stress",
                "Secondary bacterial infection"
            ],
            "remedies": [
                "Improve water quality immediately",
                "Use antibiotics for secondary infections: Tetracycline",
                "Add salt (1-2 teaspoons per gallon)",
                "Isolate infected fish",
                "Maintain optimal water parameters",
                "Increase aeration"
            ],
            "prevention": [
                "Maintain excellent water quality",
                "Reduce stress factors",
                "Quarantine new fish",
                "Proper nutrition"
            ]
        },
        "hindi": {
            "name": "व्हाइट टेल रोग",
            "type": "वायरल रोग",
            "symptoms": [
                "पूंछ का सफेद रंग बिगड़ना",
                "पूंछ सड़ना",
                "पूंछ के पंख का नुकसान",
                "सुस्ती",
                "भूख न लगना"
            ],
            "causes": [
                "वायरल संक्रमण",
                "खराब पानी की गुणवत्ता",
                "तनाव",
                "द्वितीयक जीवाणु संक्रमण"
            ],
            "remedies": [
                "तुरंत पानी की गुणवत्ता में सुधार करें",
                "द्वितीयक संक्रमण के लिए एंटीबायोटिक्स का उपयोग करें: टेट्रासाइक्लिन",
                "नमक मिलाएं (प्रति गैलन 1-2 चम्मच)",
                "संक्रमित मछली को अलग करें",
                "इष्टतम पानी के मापदंडों को बनाए रखें",
                "वातन बढ़ाएं"
            ],
            "prevention": [
                "उत्कृष्ट पानी की गुणवत्ता बनाए रखें",
                "तनाव कारकों को कम करें",
                "नई मछलियों को क्वारंटाइन करें",
                "उचित पोषण"
            ]
        },
        "kannada": {
            "name": "ವೈಟ್ ಟೈಲ್ ರೋಗ",
            "type": "ವೈರಸ್ ರೋಗ",
            "symptoms": [
                "ಬಾಲದ ಬಿಳಿ ಬಣ್ಣ ಬದಲಾವಣೆ",
                "ಬಾಲ ಕೊಳೆತ",
                "ಬಾಲದ ರೆಕ್ಕೆಯ ನಷ್ಟ",
                "ಸೋಮಾರಿತನ",
                "ಹಸಿವು ಕಡಿಮೆ"
            ],
            "causes": [
                "ವೈರಸ್ ಸೋಂಕು",
                "ಕಳಪೆ ನೀರಿನ ಗುಣಮಟ್ಟ",
                "ಒತ್ತಡ",
                "ದ್ವಿತೀಯಕ ಬ್ಯಾಕ್ಟೀರಿಯಾದ ಸೋಂಕು"
            ],
            "remedies": [
                "ತಕ್ಷಣ ನೀರಿನ ಗುಣಮಟ್ಟವನ್ನು ಸುಧಾರಿಸಿ",
                "ದ್ವಿತೀಯಕ ಸೋಂಕುಗಳಿಗೆ ಆಂಟಿಬಯೋಟಿಕ್ಗಳನ್ನು ಬಳಸಿ: ಟೆಟ್ರಾಸೈಕ್ಲಿನ್",
                "ಉಪ್ಪು ಸೇರಿಸಿ (ಪ್ರತಿ ಗ್ಯಾಲನ್ಗೆ 1-2 ಚಮಚ)",
                "ಸೋಂಕಿತ ಮೀನುಗಳನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ",
                "ಉತ್ತಮ ನೀರಿನ ನಿಯತಾಂಕಗಳನ್ನು ನಿರ್ವಹಿಸಿ",
                "ವಾಯುಚಲನೆಯನ್ನು ಹೆಚ್ಚಿಸಿ"
            ],
            "prevention": [
                "ಉತ್ತಮ ನೀರಿನ ಗುಣಮಟ್ಟವನ್ನು ನಿರ್ವಹಿಸಿ",
                "ಒತ್ತಡದ ಅಂಶಗಳನ್ನು ಕಡಿಮೆ ಮಾಡಿ",
                "ಹೊಸ ಮೀನುಗಳನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ",
                "ಸರಿಯಾದ ಪೋಷಣೆ"
            ]
        }
    }
}


def get_disease_info(disease_name, language="english"):
    """
    Get disease information in specified language
    
    Args:
        disease_name: Name of the disease
        language: Language code ('english', 'hindi', 'kannada')
    
    Returns:
        Dictionary with disease information
    """
    if disease_name not in DISEASE_INFO:
        return None
    
    if language not in DISEASE_INFO[disease_name]:
        language = "english"  # Fallback to English
    
    return DISEASE_INFO[disease_name][language]

