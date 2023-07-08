import unittest
from scryptos import RSA, rsautil
import random
import gmpy2


class TestRSA(unittest.TestCase):
    def setUp(s):
        pass

    def test_rsa(s):
        p = 10007
        q = 10009
        rsa = RSA(65537, p * q, p, q)
        s.assertEqual(rsa.d, 35910881)
        s.assertEqual(rsa.encrypt(2), 82696754)
        s.assertEqual(rsa.decrypt(82696754), 2)
        s.assertTrue(rsa.verify(2, 82696754))
        rsa = RSA(65537, p * q, p)
        s.assertEqual(rsa.q, q)
        rsa = RSA(65537, p * q, d=35910881)
        s.assertEqual(rsa.p, q)
        s.assertEqual(rsa.q, p)
        rsa = RSA(7, 17 * 19)
        s.assertEqual(
            rsa.to_pem(),
            b"-----BEGIN PUBLIC KEY-----\nMBswDQYJKoZIhvcNAQEBBQADCgAwBwICAUMCAQc=\n-----END PUBLIC KEY-----",
        )
        rsa2 = RSA.import_pem(
            b"-----BEGIN PUBLIC KEY-----\nMBswDQYJKoZIhvcNAQEBBQADCgAwBwICAUMCAQc=\n-----END PUBLIC KEY-----"
        )
        s.assertEqual(rsa2.e, rsa.e)
        s.assertEqual(rsa2.n, rsa.n)
        e = 65537
        p = 30273475826655122536846983848160550500204682688015809023335848977523483917101160672536270586442050599212388523105658958722156396123018845746524519897609762574658162037605366756637000161968957454056615351809334082634704761148089250864449954659717803085319254163373477692727609686455002524762610294656298153428381789839148893230830373303154974726530963515731262435230022596576929976932822059822740108493930213173446084979361380298692133596613850695825919575790921163545442413558822869237717221629484262019925427510325465282137171976866976076927259517451663508702630142903351619056923348092008357470407045828985216253489
        q = 25026899679257977233919368476074789189000606929670669654861099402095931044075373028105218208262296685578570826772027221115087033855782806414326752272221946923970978091610606943532328834829043818742793791659570703198031587772396469259389310570504380927982212739953474927497682617061894024658939438958024879116111361256823069627223346302696674698982817968060190185337364920943089914174684210814700656758036485832973539249277041533028779915256267817918950350116730412069682443355145574251795778432477644290721547104112473654536968151586688673598976960740253777919778270130667057007111142100646026090768853068104238449017
        rsa = RSA(e, p * q, p, q)
        c = "76c2a9315dea6500be226762980173a8d364e6409b2f00911f669628a71943ca348f67adf2ae90c9c0aa0a380793ae977483803b0062399a0dd4704f6bcab0e7240d99b1936c4dd38e029eeae0a309c8eff147d8f57214a28bd2021eb8adf262e57cd7c11c5d4405f93e3e0b2b62bf378d600bd122f4e26c25014aaf3a64b531134ace4fe2daef52ff034e14f9647040bd2aabb9c397118757c329562d1c97cb034b6ff15aa99e89850e5d2098e1a407cc58b1a45f970b965da43377d0259ebd53a91d87025774e925c4abefd9990b9fafd9b194fc87ccc25885dab31afd3f4e4cf8f71bc30129b0acd1ef6aa90e9fc736c609c16561b6975265c390de6ca99e900299fd4b3bfcaa6f1ca0104b99d19bd447a59838e799bb10cee3083131f6a580ac37353fce0c5a5bfca85e988f4a390f17d672639a2d47a7f68e9eda0ad9913440e520ab5d8a91c54de44d325d7c740952e583639dadb5b905d319a5e7a747e102ab2ad600150414567b4610df8f184ed8bdb14cb3100ee09f19dffa29a2a5d91134c5df6f48142691b18b408ebdbd68efe836ba371d06bbd64114dee64a24754822723eaa69d03aceb77448194042630c0cd0e27d5cd5181d0a78689941d5b48d2cb9d3b90368335bf70f020b50fa4729889b30dcff1c7cea2abef25ece73a8d2f6e0a5aeb8986e9e9a0559f16402012735505cc864cdc2b49d0a6ecba217"
        m = int(
            "030379ada3f4f7cff7c114fa625abe9a4bbb457eda3f3f58838f116a01300f7d44886c8639e41c52024e12c31bb6d96f",
            16,
        )
        s.assertEqual(rsa.decrypt_PKCS15(int(c, 16)), m)

    # Common Modulus Attack
    def test_common_modulus(s):
        n = 100160063
        e1 = 65537
        e2 = 65539
        rsa1 = RSA(e1, n)
        rsa2 = RSA(e2, n)
        m = random.randint(2, n)
        c1 = rsa1.encrypt(m)
        c2 = rsa2.encrypt(m)
        s.assertEqual(rsautil.common_modulus(rsa1, rsa2, c1, c2), m)

    def test_common_private_exponent(s):
        from scryptos.wrapper.common import check

        if check("gp") or check("fplll") or check("gap"):
            # Common Private Exponent Attack
            # ek, nk from reference paper
            e1, n1 = 587438623, 2915050561
            e2, n2 = 2382816879, 3863354647
            e3, n3 = 2401927159, 3943138939
            rsa1 = RSA(e1, n1)
            rsa2 = RSA(e2, n2)
            rsa3 = RSA(e3, n3)
            s.assertEqual(rsautil.common_private_exponent([rsa1, rsa2, rsa3]), 655)

    def test_hastads_broadcast(s):
        # Hastad's Broadcast Attack
        e = 3
        n1 = 100160063
        n2 = 100761443
        n3 = 101284087
        rsa1 = RSA(e, n1)
        rsa2 = RSA(e, n2)
        rsa3 = RSA(e, n3)
        m = random.randint(2, n1)
        c1 = rsa1.encrypt(m)
        c2 = rsa2.encrypt(m)
        c3 = rsa3.encrypt(m)
        s.assertEqual(rsautil.hastads_broadcast([rsa1, rsa2, rsa3], [c1, c2, c3]), m)

    def test_wiener(s):
        # Wiener's Attack
        e = 17993
        n = 90581
        rsa = RSA(e, n)
        rsa2 = rsautil.wiener(rsa)
        s.assertEqual(rsa2.d, 5)
        # Issue #3: bug in wiener function
        e = 49446678600051379228760906286031155509742239832659705731559249988210578539211813543612425990507831160407165259046991194935262200565953842567148786053040450198919753834397378188932524599840027093290217612285214105791999673535556558448523448336314401414644879827127064929878383237432895170442176211946286617205
        n = 109676931776753394141394564514720734236796584022842820507613945978304098920529412415619708851314423671483225500317195833435789174491417871864260375066278885574232653256425434296113773973874542733322600365156233965235292281146938652303374751525426102732530711430473466903656428846184387282528950095967567885381
        rsa = RSA(e, n)
        rsa2 = rsautil.wiener(rsa)
        s.assertEqual(
            rsa2.d,
            21780352155588618020563641971337344243907391969899764877790673891831527301137,
        )

    def test_franklin_reiter(s):
        # Franklin-Reiter Related Message Attack
        e = 255
        n = 100160063
        rsa = RSA(e, n)
        m1 = 86452943
        m2 = 7 * m1 + 3
        c1 = rsa.encrypt(m1)
        c2 = rsa.encrypt(m2)
        s.assertEqual(rsautil.franklin_reiter(rsa, 7, 3, c1, c2), m1)

    def test_fault_crt_signature(s):
        # Boneh-DeMillo-Lipton's CRT Fault Attack
        e = 65537
        n = 100160063
        m = 12345
        fault_sig = 82770107
        rsa = RSA(e, n)
        rsa2 = rsautil.fault_crt_signature(rsa, m, fault_sig)
        s.assertEqual(max(rsa2.p, rsa2.q), 10009)

    def test_modulus_fault_crt(s):
        from scryptos.wrapper.common import check

        if check("gp") or check("fplll") or check("gap"):
            n = 139597781215932958403361341802832587199
            e = 65537
            rsa = RSA(e, n)
            fault_sigs = [
                1058535326842046404366164623977343348220096515298415971420,
                498516681624023022157905434041816372788280365785800693627,
                804996362997244807580066976356636401798047106638276618248,
                486102002898098045301788623412192711614890707650168500297,
                1109646572715192904427320549147799213950859213551899817975,
            ]
            rsa2 = rsautil.modulus_fault_crt(rsa, fault_sigs)
            s.assertEqual(max(rsa2.p, rsa2.q), 14741565978953596877)

    def test_ciphertext_homomorphism(s):
        p = 10007
        q = 10009
        rsa = RSA(65537, p * q, p, q)
        s.assertEqual(rsa.d, 35910881)
        s.assertEqual(rsa.encrypt(2), 82696754)
        s.assertEqual(rsa.decrypt(82696754), 2)
        c = rsa.encrypt(2)
        s.assertEqual(rsa.decrypt(c * c), 4)
        s.assertEqual(rsa.decrypt(2 * c), 4)
        s.assertEqual(rsa.decrypt(c * 2), 4)
        s.assertEqual(rsa.decrypt(-c * -2), 4)
        s.assertEqual(rsa.decrypt(-c * -2), 4)
        with s.assertRaises(AssertionError) as cm:
            rsa.decrypt(c + 1)
        with s.assertRaises(AssertionError) as cm:
            rsa.decrypt(c - 1)

    def test_lsb_oracle(s):
        p = 10007
        q = 10009
        rsa = RSA(65537, p * q, p, q)

        def oracle(c):
            o = rsa.decrypt(c) % 2
            return o

        s.assertEqual(rsautil.lsb_oracle(rsa, rsa.encrypt(12345678), oracle), 12345678)
        random.seed(12345)
        for _ in range(20):
            m = random.getrandbits(24)
            print("[+] m: {}".format(m))
            s.assertEqual(
                rsautil.lsb_oracle(rsa, rsa.encrypt(m), oracle, quiet=True), m
            )
