import random
import time

def charger_vocabulaire(fichier):
    vocabulaire = {}
    verbes_francais = []
    article_map = {'m': 'der', 'f': 'die', 'n': 'das'}

    with open(fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            if '=' in ligne:
                allemand_part, francais = ligne.strip().split(' = ')
                mots = allemand_part.split()

                # Cas où il n’y a pas de genre (par ex. pour un verbe)
                if len(mots) > 1 and '(' in mots[1]:
                    if len(mots) > 3:
                        mot_allemand = mots[0] + " " + mots[1] + "aaa"
                        genre = mots[2].strip('()')
                        article = article_map.get(genre, '')
                        allemand_complet = f"{article} {mot_allemand}".strip()
                    else:
                        mot_allemand = mots[0]
                        genre = mots[1].strip('()')
                        article = article_map.get(genre, '')
                        allemand_complet = f"{article} {mot_allemand}".strip()
                    verbes_francais.append(francais)
                else:
                    allemand_complet = mots[0]

                vocabulaire[francais] = allemand_complet
    return vocabulaire, verbes_francais

def calculer_points(reponse, correct, temps, est_nom):
    if temps < 5:
                # Vérifier si le déterminant est correct
        mots_reponse = reponse.split()
        mots_correct = correct.split()
        if len(mots_reponse) > 0 and len(mots_correct) > 0 and mots_reponse[0].lower() != mots_correct[0].lower():
            return 0.5 if mots_reponse[1:] == mots_correct[1:] else 0
        return 0.75 if reponse.lower() == correct.lower() else 0

    if est_nom:
        # Vérifier si le déterminant est correct
        mots_reponse = reponse.split()
        mots_correct = correct.split()
        if len(mots_reponse) > 0 and len(mots_correct) > 0 and mots_reponse[0].lower() != mots_correct[0].lower():
            return 0.5 if mots_reponse[1:] == mots_correct[1:] else 0

    return 1 if reponse.lower() == correct.lower() else 0

def poser_question(vocab, verbes_francais, score_total, erreurs, total_possible_points):
    if random.random() < 0.25:
        # 25% du temps, demander la traduction de l'allemand vers le français
        francais, allemand_correct = random.choice(list(vocab.items()))
        est_verbe = francais in verbes_francais

        if est_verbe:
            choix = random.sample(verbes_francais, 3)
        else:
            choix = random.sample(list(vocab.keys()), 3)

        if francais not in choix:
            choix[random.randint(0, 2)] = francais
        random.shuffle(choix)

        print(f"Traduisez en français : '{allemand_correct}'")
        for i, option in enumerate(choix, 1):
            print(f"{i}. {option}")

        debut = time.time()
        reponse = int(input("Votre réponse (numéro) : ").strip())
        temps_ecoule = time.time() - debut

        if choix[reponse - 1] == francais:
            print("✅ Correct !")
            score = 1  # Pas de points partiels pour la traduction vers le français
        else:
            print(f"❌ Faux. La bonne réponse était : {francais}")
            score = 0
            erreurs.append((allemand_correct, francais))
    else:
        # 75% du temps, demander la traduction du français vers l'allemand
        francais, allemand_correct = random.choice(list(vocab.items()))
        print(f"Traduisez en allemand : '{francais}'")

        debut = time.time()
        reponse = input("Votre réponse (ex: der Stuhl) : ").strip()
        temps_ecoule = time.time() - debut

        est_nom = ' ' in allemand_correct
        score = calculer_points(reponse, allemand_correct, temps_ecoule, est_nom)

        if score > 0:
            print("✅ Correct !")
        else:
            print(f"❌ Faux. La bonne réponse était : {allemand_correct}")
            erreurs.append((francais, allemand_correct))

    score_total += score
    print(f"Points obtenus : {score}")
    print(f"Score total : {score_total}/{total_possible_points}")
    return score_total, erreurs

def repeter_erreurs(erreurs, vocab, verbes_francais, score_total, total_possible_points):
    if not erreurs:
        return score_total

    nouvelles_erreurs = []
    for francais, allemand_correct in erreurs:
        for _ in range(random.randint(1, 5)):
            continuer = input("\nVoulez-vous continuer ? (o/n) : ")
            # Poser une question intermédiaire avant de répéter l'erreur
            question_intermediaire = random.choice(list(vocab.items()))
            print(f"Avant de répéter votre erreur, traduisez en allemand : '{question_intermediaire[0]}'")
            debut = time.time()
            reponse_intermediaire = input("Votre réponse (ex: der Stuhl) : ").strip()
            temps_ecoule = time.time() - debut

            est_nom_intermediaire = ' ' in question_intermediaire[1]
            score_intermediaire = calculer_points(reponse_intermediaire, question_intermediaire[1], temps_ecoule, est_nom_intermediaire)

            if score_intermediaire > 0:
                print("✅ Correct !")
            else:
                print(f"❌ Faux. La bonne réponse était : {question_intermediaire[1]}")
                erreurs.append((question_intermediaire[0], question_intermediaire[1]))

            score_total += score_intermediaire
            print(f"Points obtenus : {score_intermediaire}")
            print(f"Score total : {score_total}/{total_possible_points}")



        continuer = input("\nVoulez-vous continuer ? (o/n) : ")
        # Maintenant, reposez la question où l'utilisateur a fait une erreur
        print(f"Traduisez en allemand : '{francais}'")
        debut = time.time()
        reponse = input("Votre réponse (ex: der Stuhl) : ").strip()
        temps_ecoule = time.time() - debut

        est_nom = ' ' in allemand_correct
        score = calculer_points(reponse, allemand_correct, temps_ecoule, est_nom)

        if score > 0:
            print("✅ Correct !")
        else:
            print(f"❌ Faux. La bonne réponse était : {allemand_correct}")
            erreurs.append((francais, allemand_correct))

        score_total += score
        print(f"Points obtenus : {score}")
        print(f"Score total : {score_total}/{total_possible_points}")
            

    return score_total

def quiz(vocab, verbes_francais):
    continuer = "o"
    score_total = 0
    erreurs = []
    total_possible_points = 0
    n = 0

    while continuer.lower() != "n":
        score_total, erreurs = poser_question(vocab, verbes_francais, score_total, erreurs, total_possible_points)
        n += 1
        total_possible_points += 1
        if erreurs and (n > 5 or n == random.randint(1, 5)):
            score_total = repeter_erreurs(erreurs, vocab, verbes_francais, score_total, total_possible_points)
            erreurs = []  # Réinitialiser les erreurs après les avoir répétées
            
            n = 0
        continuer = input("\nVoulez-vous continuer ? (o/n) : ")

    print(f"Merci d'avoir joué ! Votre score final est : {score_total}/{total_possible_points} Viel Erfolg ! 🇩🇪")

if __name__ == "__main__":
    vocabulaire, verbes_francais = charger_vocabulaire("vocabulaire.txt")
    quiz(vocabulaire, verbes_francais)