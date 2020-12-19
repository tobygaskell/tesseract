import testing, random, unittest
import read_from_sql as a 


class Test_read_from_sql(unittest.TestCase): 

    def test_read_choices(self): 
        num = 2
        testing.clear_choices() 
        testing.add_dummy_choices2(num)

        self.assertEqual(a.read_choices(1), {'Toby':'Manchester United','Val':'Manchester United', 'Dylan':'Manchester United' })
        self.assertEqual(type(a.read_choices(random.choice(range(1,num)))), type({}))
        self.assertEqual(a.read_choices(num+1), 'No Choices Made')

    # def test_read_added_info(self):
    #     testing.clear_added_info()
    #     tetsing.add_dummy_added_info()

    #     self.assertEqual()

if __name__ == '__main__': 
    unittest.main()