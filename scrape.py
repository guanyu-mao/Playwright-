import os
import importlib
import time
import re
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# load custom functions needed for this script
os.chdir('C:\\Playwright\\Playwright%20exporter')  # Change this to your project directory
import src.scraper_functions as scp

importlib.reload(scp)                                                                                                                            
# load configuration file (user, password, dashboard_url, download location)
load_dotenv(override=True)


# List of URLs for resource group cost views
resource_group_urls = [
    "https://portal.azure.com#@Ontariogov.onmicrosoft.com/blade/Microsoft_Azure_CostManagement/Menu/open/CostAnalysis/scope/%2Fsubscriptions%2Fd491ccef-9bda-4adf-a63e-cbfc63d9b368%2FresourceGroups%2Fazr-prd-mx-0604-wrk-cc-rgp-bipdde-0000-preprod/view/H4sIAAAAAAAAA4VSy27bMBD8F57N2IUNo87Nj9Qw0MqBpfQSFMGKXClEJFJdkm1Uw%2F%2FepR9J2hzCG3dndmc43AsVidCqXlyL5XwlBkJDwB3YGrnyFXz45mx45PrPiMSovQh9l3pzFSI0S%2BfDiQQ5htSuCWxsgExIM4%2FspmcI1DVhDcE4e5ziwpnNFwttGnkeVkWrTjCRx1YcBq%2Fgu3z1Hz5V3lOY4x0FY2txfb8X2hBe%2BuAVWp06g8uchWkaLpycHn4M2IOL3YV89rsyLVqfZrzwduhdJIUbzawkkyEVnXqZs5ikq0cg9igKKBtMz6BUbPl9AmquVtD4VO3MLxc8r%2BPlXrnjQh9Lr8h0Sbcf6snsk1JYyVmpQU5AVxKmY5SqrNR0rGflePp5SGdB66TfD%2BEPyY60bJ%2FlaDqayN%2F0JJWSVHeyNJ3WKEd8GIIdOc0ynjrj33peRF1jisQkscttXjxk8%2B%2Bb9bzY7q4Wd6v1TfGwvS022yy%2FyrbZDSPRJqMMDxSRr8%2BBXxv1LbEpDgT92%2Fw%2BHshJvqj54jhFOH6Rf7akxLTxXQN99voxFv0lHnH4C0SKUPTnAgAA",
    "https://portal.azure.com#@Ontariogov.onmicrosoft.com/blade/Microsoft_Azure_CostManagement/Menu/open/CostAnalysis/scope/%2Fsubscriptions%2Fd491ccef-9bda-4adf-a63e-cbfc63d9b368%2FresourceGroups%2Fazr-prd-mx-0604-wrk-cc-rgp-bipdde-0000-preprod/view/H4sIAAAAAAAAA4VT204bMRD9Fz%2BvCShRVHjLhUZRyyYigT4gFM3as4sVx3Z9AQLKv3e8Sbi0ldiX1c652HNm9pWJ5D0asWUXbDQYs4JJiHgNpkGq%2FIQQr6yJD1T%2FndAT65XFrcvYQMQEemRD3ItggTHDjQeTNHgVs2er1luiQNN4bCAqa1oXGw9q%2BjCwyZYHszoZsaexRdqwXfFOvlmM%2F%2BLnyr8S0gTrozINu7h7ZVJ5POIQBBqZkeLoM1RaU2Hf6e6%2BoB5sckfxod%2Bx2qAJ2eNNd43BJi9wKltVrXREn%2B%2B3hCbkd7nnCZ0CIa2qYDOHHqIlIptms1vQCYl%2Bx1QM8MLDA3iUXOgQPRdPzkoivUMH5IwgnrH7Xe420u1qvz%2ButAZzaoLYFC%2FdptL5YBAibWg0ESVVa9AhV516tDF80ekC%2FaMS2PazK96Y1OcP3L7T8hpUXol1UCZEMAKdtVrJj5r%2FuF9hzi1HGIRtSSFVQXjl8sxCR%2FbOz4TAmp9XEngPZM2h30Uuqlr0u%2FK86va%2FdfxhGJM8u9CBF88dhbV55qf90x5%2F8msuBPeN45VyUiI%2FpYco6Hyb8NqpTykMk2wwr6PKaY1mi%2BWqHNxOJ4Pl7PpkeDOeXC5Xs%2FlyOisXJ%2BWsvCQmmpw00aNPSJ%2FPkTYN5dxTU7SMGD7u7teGuw%2Bpfbe0wdD%2BHp9OyaFJFZyG7WHZRr9W8%2Fnlavw2ilX7W%2B3%2BAAEWNSjrAwAA",
    "https://portal.azure.com#@Ontariogov.onmicrosoft.com/blade/Microsoft_Azure_CostManagement/Menu/open/CostAnalysis/scope/%2Fsubscriptions%2Fd491ccef-9bda-4adf-a63e-cbfc63d9b368%2FresourceGroups%2Fazr-prd-mx-0604-wrk-cc-rgp-bipdde-0000-preprod/view/H4sIAAAAAAAAA91UXU%2FbMBT9K8jPNWEDVWNvpQVUCdqOFPaAUOTYN8EiscO1XSio%2F33XaQqFiSFtb%2BtDJd97zsn9fmYyIIKRS%2FadDQcj1mNKeLgQpgSynAnnz63xt2S%2FD4CEemZ%2B2UTfQPogqqF1fk0SKfjoLlGYUAnUPmq27GpJEFGWCKXw2ppWxfqOTQ8j6ijZiRXByDWMpaFmq94r%2BDIdvcNHy%2B8U4jiLXpuSfb9%2BZkojbPzCSTAqenobnSNdVWRYZ7q66VEONjQbcpfvSNdgXNR44V2AswEljFXLKnTlAWN8A6Na6gvHRetkzUoBF1pC%2B%2BqxaQMovCUaG0fpK1EFIPg1GzwFhJ0RVXbnREiCLHcWXwmR%2FjhrrblwUeAVlqOWdy4iCCyogTdUhw%2BC2Ar9TzEkLuROom5i8VyiDg6%2FSAkFP8yV4AdCFVz094HLvJD9fXWY7%2Fe%2FJdhJt0V0iXhC3qDi9SPf6%2B8d8Ae841JyLBue60Yp4Hv0Iwg0aFVCfwutAF1Sa4nW2cLvuvsqcVS1aN3IbWtt6xCW53W%2FfExUVyOXRH90qJzLB65qrgvK8v%2FLjUY2s02m6tj52HzmqfcFrls%2BsQbiMslbgbR1bC7yKg6QkDLUtLEeaGhZIap2rBq9sN59sgDnEAc%2BDtnHmG7c5%2FpT5Lt1ctK2yH9o0%2BnftIkCumv0m9SPgiohniYdSzScpvNsMrganw7m04vdo8vR6fE8m87m4%2Bkk3Z1MJ8eEBBPLS3CPAej56OnqgJohJUWHCdz2HftccLVVuhNL10y0p%2FLNV2LRlHZNJZbdlg9%2FZrPZcUYXY3MwsvbGrn4BLHzP8fgFAAA%3D",
    "https://portal.azure.com#@Ontariogov.onmicrosoft.com/blade/Microsoft_Azure_CostManagement/Menu/open/CostAnalysis/scope/%2Fsubscriptions%2Fd491ccef-9bda-4adf-a63e-cbfc63d9b368%2FresourceGroups%2Fazr-prd-mx-0604-wrk-cc-rgp-bipdde-0000-preprod/view/H4sIAAAAAAAAA41T204bMRD9lcrPMZeCosJbSCiK2iYRG3hBKJq1ZxcrG9sd25QQ5d8ZbwIJRb34bTznnJk5Hq%2BESkRo1VKci35vIDpCQ8RrsDXyzXcI8Yez8YHvfyYkRq1EXPqc66mYoOm7EDckKDDmdE1gUwNkYtYcgGmWDIC6JqwhGmdbDRe3XA4sLLLgVqpKVm1gokgLse7swDfF4Dd8vvlIYU5wFI2txfndSmhD%2BJqHoNDqnOm86twEqHHAU4v1fYfbd8m%2FMrejTqH%2BhssdQzUpRKQ2ypzKNBzm1npWt8SBWaANXDLk29GGViA9GoVt1BFjjwTRMU0MLce30CRk%2BJ3oPSfCT9wRlGTUPIh7nmiVu9hX22%2Fib2omBniW4QFIS9WESMcSlS6N9E4z8EP6816aC%2BfaIvI4FW3qjpzF%2FCqKKTFPFUHNUfddkxa5MiiVFrwAEdkKUUETcn%2FePLoY%2FtvUzh9h%2Bs0WY0MEq9A71yjCPL3R%2B9S3R9ixrzG4RAqHun24oFyLDKkMiozPSxIO9enZsVJYybNSgzwFXUnonqBUZaW6J%2FqsPOl%2BOaSt0lXel3AIzyQ9W7h4kkfdo1P5i%2BZSKUm1l6XxWqM84sMQ9NT6PvfmnR0XSdeY999k2%2FrjYjob9W6HV73p%2BPrg4mZwdTmdjSfT4XhUHIzGo0tGooWyyS5HSsjhU%2BTVRj0hHoq3H8P%2BZ%2Fm34HrPuq%2BOvwy0%2F%2FFdlWyaNsE3sNyu4bDoD4vZZHI52y3srP3K6xdJHiozXQQAAA%3D%3D",
    "https://portal.azure.com#@Ontariogov.onmicrosoft.com/blade/Microsoft_Azure_CostManagement/Menu/open/CostAnalysis/scope/%2Fsubscriptions%2Fd491ccef-9bda-4adf-a63e-cbfc63d9b368%2FresourceGroups%2Fazr-prd-mx-0604-wrk-cc-rgp-bipdde-0000-preprod/view/H4sIAAAAAAAAA4VT224aQQz9lWqemVxKhJq8LZAi1AZQIHmJIuSd8W6mWWa2c0lDEP9ee4FAErXZt7HPOWsf2yuhkvdo1VJciF7WFy2hIeI12BIp8hNCvHI2PlD8d0JPqJWIy5pzmYoJqp4LcUOCKUZOlx5sqsCbyJoNu1oSBMrSYwnRONuouLhl08PCgiW3YkWyagMT07QQ69YefDPtv8Nz5COFOMH5aGwpLu5WQhuPuzwEhVZzprXT6ZqqosCm0%2FV9i3pwqd6Rt%2F32zQJtYI1X3jUGl7zCoW5Yhakieq4vs7qhvnICR0cb1hT9k1HYvFpiXKOH6Igmhix9C1VCgt%2BJ7CV5%2FNInZ3Nv1GMQ99TWSsygPFRTVQr0V%2FuZmokBXmR4AK%2BlqkL0X2UAWTtNqA%2B50%2Fe5Xy7fsz5GGc%2FlcYUiUtOF31Q3chZ5gIq0adJUfF5xnaBUWtCWRCSjRAFV4GhtnlwMh6ZTsz9wuXf8sFs249%2BzuUKexf8xPaqqxBnneX5BuQYZUh6UNzUvTDjWZ%2BenSmEhz3MN8gx0IaHTRqnyQnXa%2Bjxvd74d%2B%2B0mDHhxwjG8eFmTmYtnedI5OZN%2F%2FKNUSvqylrmptUZ5Qh9BsPaNy4%2B1edN3N%2BkS%2BRYM%2B9MbT2fzUXY7HGSz8fVR96Y%2FuJzNx5PZcDyaHo3Go0tComVvCR59Qno%2BR1pz1BNPTdElYDg8nM8F1wfWfXd0PtDc5pu%2FsGnahLqC5W63s%2FlkcjnfL%2B28uen1X66DlGpoBAAA",
    "https://portal.azure.com#@Ontariogov.onmicrosoft.com/blade/Microsoft_Azure_CostManagement/Menu/open/CostAnalysis/scope/%2Fsubscriptions%2Fd491ccef-9bda-4adf-a63e-cbfc63d9b368%2FresourceGroups%2Fazr-prd-mx-0604-wrk-cc-rgp-bipdde-0000-preprod/view/H4sIAAAAAAAAA91VTU8bMRD9K5XPMUsVFBVuC0mjSDRJs4ELQpHXnl0svOvFH4EU5b8zs0loSgX040YOK3nmvTeeif38yGR0Dmq5YifsLO2zDlMiwEzUJWDkXPjwzdbhBuN3ERyiHllYNZRLZYjCnFkfNiSRQaB06UQdjXA6kGbLNiuEiLJ0UIqgbd2q2LBl46IWFUluxYpYyw2MZbFi685P8EXWf4GnyO8U5Hjrgq5LdnL1yJR2sMsLL6FWlOnsdE61MRjYdLq%2B7mAPNjY78rbfvq6g9qTxzJuBt9FJGKmWVWgTwNH%2B0lq11GeOp%2Bh4w8rALbWEdtVhkwacCBZpbETSl8JEQPgVy76ff%2BrjXHPhgV1jS6%2Fo7e3iLbnEx9xLpxuag0%2FU0fFnKaHgx7kS%2FEiogoteF7jMC9nrquO82%2FuSuK10Ow%2BfiB%2BON07x6oEf9g6P%2BL275VJyVzY8141SwA%2FxhxBonFUJfpZagfNJpaWz3hbhwN%2BZxOMAKLqT29fa10Esz6te%2BZCo7Rh8QnlKqJzLVeEFv4fc60CT%2FNgNLhQsP2KTXuTac6FurPyTQz6kHt69On%2FXItWl0ixg5cJtCo5tDWQ98kY49Cg2F7mhokLKWKG%2FBcArzgphPEUbvbTBv2MX24s%2F12gS1OjrSDK21BgrW7ucRbNxi7dJL9zIS9si%2F%2BPADP%2FlwOCGbhv9yyxOoyqBnF3TzM4m2XwxTi9Hw3Q%2BmR2cXvSHg%2FliMp2PJuPsYDwZDxAJNc0b4cFFwOVDQNMGNXXYFPo6%2BP1n4H3B9d7ovlp8DET70jxXaf9HmprSvjFitbPqdDGdDhboxDsjXrRv1PoJm76iyzgHAAA%3D",
    "https://portal.azure.com#@Ontariogov.onmicrosoft.com/blade/Microsoft_Azure_CostManagement/Menu/open/CostAnalysis/scope/%2Fsubscriptions%2Fd491ccef-9bda-4adf-a63e-cbfc63d9b368%2FresourceGroups%2Fazr-prd-mx-0604-wrk-cc-rgp-bipdde-0000-preprod/view/H4sIAAAAAAAAA4VTXVMiMRD8L3kmikpRh28gHkWdshSgL5ZFzSaza86Q7OXjTrT47052V8TzrOOFynT3ZKd78sJEdA6N2LJzdjEcsw6TEHABpkSqXIEP19aEB6r%2FiuiI9cLCtkrYUIQI%2BsL60IhgiSHBpQMTNTgVUs9arbdEgbJ0WEJQ1tRdbGjVdDCwSS3bZkU0oqGxZdywXeedfLMc%2F8VPlc8S0njrgjIlO797YVI5fMPBCzQyIZ23PiOlNRWaSXf3HZrBxupN3M47Vhs0PvXY6xbobXQCp7JWFUoHdOn7VlD69D9reEJHT0it6rCsQgfBEpFNU7Nb0BGJfsdU8PDMhfbBcfp8p%2FlPm9fHdYTkzNeE0w8M%2FwBONryTllhZuYdJ9AH8DJy2wP0uWRlo9MI1s8yswRSJoCsoOxo112kqECJuKPeAkqoFaJ%2Bqlfptgz%2B0kaz5gdt3Dw%2B92XW%2BpKUFy50Sj14ZH8AIbDKSh6J%2FRHSNKZKUjhe2JvmYe%2BFUldbBH8ve4EQILPggl8B7IAsO%2FTPkIi9E%2F0wO8rP%2Bt2PX5jxJV%2FpjeHa8In83T7zb7%2Fb4H%2FfIheCurHiuKimRd%2BlHFKxc7fpjpT54MIqyxDqt5NVFtlytZ8Pb6WS4yhZHo5vx5HK1zuaraTZbHs2y2SUx0SSfiR5cRDo%2BBVpilHNHQ9Geoz98Fv9vuDtw7bulxwH1y9vfUueXXJPKVxq27SIvs8Xiaj2fX67H%2BzzW9avdvQIrhjLVSgQAAA%3D%3D",
    "https://portal.azure.com#@Ontariogov.onmicrosoft.com/blade/Microsoft_Azure_CostManagement/Menu/open/CostAnalysis/scope/%2Fsubscriptions%2Fd491ccef-9bda-4adf-a63e-cbfc63d9b368%2FresourceGroups%2Fazr-prd-mx-0604-wrk-cc-rgp-bipdde-0000-preprod/view/H4sIAAAAAAAAA91XwU7bQBD9lWrPWUwFikpvgVAUKU0CDlwQssa7Y7PC9pqddSBF%2BffO2gkNrVqq9uYcInnmvZd9s4705kWoxjms1Fp8FmejsRgIDR6voMqRK1Mg%2F9VW%2Fp7rjw06Rr0Iv65Db6R8A8WZJd%2BRIEYf2rmDqinAGR80W3axZgjkucMcvLFVq2L9ls0PFZRBciuWNZXqYCJuSrEZ%2FABfx%2BOf8KHyK4U5ZJ03VS4%2B374IbRzu%2BkAKKx06g53OqSkKLnRON3cD9mCbekfe%2Bh2bEisKGq%2B8KyTbOIUT3bIyU3h04XyjSrfUVw6F6qxjxehWRmH7NBDzGh14yzQxCdI3UDTI8FsRX04%2FjHmuKRCKO7b0G729U%2FxJLqImJeVMHeZAkT4%2B%2BagUZvIk1SCPQWcShkcoVZqp4ZE%2BSY%2BGnyK3lW7nQRF8c7J2WpbP8nB4eCyf3INUSrq8lqmptUZ5yB%2BGYO2sjvhrZTQ6ikqjnCWb%2BQN6LCLiAYTqTm5fa1%2BHsTIth%2FlzpLdjoCj0Q0OnEvj4zoMxln32zp3i9y%2BxdaLLXrp7krqUJuult3VGIJ8wJeOx9wYTjas%2BmkSlGd5HZwZ6%2BVYaUob6aKxED6HBeQTJdwGkdyYt9PT2aiCqOYraqpf%2FOoLUkAR9b1XIqCGmCs8pNXNdOJ0F31xT9%2BA46oslpEUYBIe3puQ1wSMnZZFBQaFam5X19E7q3s%2FPIRS%2Fn8%2BnVnV7x9%2FBt3GelG2R%2F3FlF%2F9yZXygh9q8mcJpo3MMq5EJ0zqbx8tkNrqZXIyW86uD0%2BvxxfkymS%2BWk%2FksPpjNZ%2BeMxCpMmuHeNciPz563HtQLx6Z4MULa36PeF9zsje6L5W0K2lXtza%2BEoWlDdQHr3apzOd1tMMlicZ60C97mOwwuyHR1DgAA",
    "https://portal.azure.com#@Ontariogov.onmicrosoft.com/blade/Microsoft_Azure_CostManagement/Menu/open/CostAnalysis/scope/%2Fsubscriptions%2Fd491ccef-9bda-4adf-a63e-cbfc63d9b368%2FresourceGroups%2Fazr-prd-mx-0604-wrk-cc-rgp-bipdde-0000-preprod/view/H4sIAAAAAAAAA4VTXW%2FaMBT9K5Ofk8IEQqNvfA2hrQkiaV%2BqCjn2TWoR4uza7kpR%2FvuuEyh0lba83etzTnxOTo5MOESoxIHdstlkzgImuYUNrwqgzU9u7J2u7DPtfzlAQh2ZPdT%2BbCKs4%2BVMG9uReALWHxfIK1dyVNZrtuzyQBBeFAgFt0pXrYq2JzYNFd97yZNY7irRwVji9qwJLuD7ZP4X3m8%2BU4hjNFpVFez28cikQjifcyOgkv4kOOtMVVnSonPaPAXkQbv6TD75nas9VMZrvPM2YLRDASvZsnJVWkB%2Fv3es8VPUoRPAFyWgnQIW14DcaoKzlZd84KUDgj%2ByyZtD%2BDKnRDNUYmfYU%2BP9WNLMsZOKdAU%2BF%2FHMkQJkKc9KL8qFcHsK34Kkbc5L47e1etHWXHtJefEDDhcjAqG9SxP8y%2B4deHtXmE8ypTMEaScfiBG6xRmXGYGq9l%2FA9ORw%2FFUIyMNxJnk45DIP%2BWgAochyMRrIcTYYfevhKdql%2FxKmx98wrFGG%2B9ewP%2BoPw9%2B4C4UIsajDTNVSQtinhyBQo5Z0o12tPjieOlmAL5fyycziJN1Gk4fVcpLGm5vp%2FXy5SLfxOl3FUXITxdGCkFD5VAlu0QGNr5Z6A3KNZIqqBea6if8XbK6C%2B66pj7wt%2B4e3%2BNCkMnXJD6fSXGqwXa8X21mX8Lb9U5o%2FTb1qtb4DAAA%3D",
    "https://portal.azure.com#@Ontariogov.onmicrosoft.com/blade/Microsoft_Azure_CostManagement/Menu/open/CostAnalysis/scope/%2Fsubscriptions%2Fd491ccef-9bda-4adf-a63e-cbfc63d9b368%2FresourceGroups%2Fazr-prd-mx-0604-wrk-cc-rgp-bipdde-0000-prod/view/H4sIAAAAAAAAA4VSy27bMBD8F57N2IUNo87Nj9Qw0MqBpfQSFMGKXClEJFJdkm1Uw%2F%2FepR9J2hzCG3dndmc43AsVidCqXlyL5XwlBkJDwB3YGrnyFXz45mx45PrPiMSovQh9l3pzFSI0S%2BfDiQQ5htSuCWxsgExIM4%2FspmcI1DVhDcE4e5ziwpnNFwttGnkeVkWrTjCRx1YcBq%2Fgu3z1Hz5V3lOY4x0FY2txfb8X2hBe%2BuAVWp06g8uchWkaLpycHn4M2IOL3YV89rsyLVqfZrzwduhdJIUbzawkkyEVnXqZs5ikq0cg9igKKBtMz6BUbPl9AmquVtD4VO3MLxc8r%2BPlXrnjQh9Lr8h0Sbcf6snsk1JYyVmpQU5AVxKmY5SqrNR0rGflePp5SGdB66TfD%2BEPyY60bJ%2FlaDqayN%2F0JJWSVHeyNJ3WKEd8GOI0a3jqjH9reBF1jSkPk5Qut3nxkM2%2Fb9bzYru7Wtyt1jfFw%2Fa22Gyz%2FCrbZjeMRJtcMjxQRL4%2BB35q1LfEjjgN9G%2FD%2B3ggx%2Fii5ovjCOH4P%2F7ZkuLSxncN9Nnrr1j0l2zE4S%2FS9hUw5AIAAA%3D%3D",
]

downloads_dir = r"C:\azure_tables"
os.makedirs(downloads_dir, exist_ok=True)

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)
context = browser.new_context()
page = context.new_page()

user = os.getenv('user')
password = os.getenv('password')

# If login is required, uncomment and use your login function
login_url = "https://portal.azure.com#@Ontariogov.onmicrosoft.com"
dashboard_url = "https://portal.azure.com#@Ontariogov.onmicrosoft.com"
page = scp.log_me_in(page=page, user=user, password=password, login_url=login_url, dashboard_url=dashboard_url)


page.pause()
failed_urls = []

for url in resource_group_urls:
    print(f"Navigating to: {url}")
    page.goto(url)
    page.wait_for_load_state()
    time.sleep(5)

    try:
        # Wait for the iframe to be attached and visible
        iframe_locator = page.locator('iframe[name="CostAnalysis.ReactView"]:visible')
        iframe_locator.wait_for(state="attached", timeout=30000)
        frame = iframe_locator.content_frame

        page.locator("iframe[name=\"CostAnalysis\\.ReactView\"]").content_frame.locator("iframe[title=\"frame\"]").content_frame.get_by_role("button", name="Granularity: Monthly ").wait_for(state="visible", timeout=20000)
        page.locator("iframe[name=\"CostAnalysis\\.ReactView\"]").content_frame.locator("iframe[title=\"frame\"]").content_frame.get_by_role("button", name="Granularity: Monthly ").click()
        print("Granularity dropdown clicked (generic selector).")

        page.locator("iframe[name=\"CostAnalysis\\.ReactView\"]").content_frame.locator("iframe[title=\"frame\"]").content_frame.locator("#Daily").wait_for(state="visible", timeout=10000)
        page.locator("iframe[name=\"CostAnalysis\\.ReactView\"]").content_frame.locator("iframe[title=\"frame\"]").content_frame.locator("#Daily").click()
        print("Daily option selected.")
        time.sleep(5)  # Wait for data to refresh after changing granularity

        # Wait for the Download menu item to be visible and click
        download_menu = frame.get_by_role("menuitem", name="Download")
        download_menu.wait_for(state="visible", timeout=30000)
        download_menu.click()
    except Exception as e:
        print(f"ERROR: Download button not found or not clickable: {e}")
        failed_urls.append(url)
        continue

    try:
        # Wait for the Excel radio button to be visible and click
        excel_radio = page.get_by_role("radio", name="Excel")
        excel_radio.wait_for(state="visible", timeout=30000)
        excel_radio.click()
    except Exception as e:
        print(f"ERROR: Excel radio button not found or not clickable: {e}")
        failed_urls.append(url)
        continue

    try:
        # Wait for the Download data button to be visible and click, then handle download
        download_button = page.get_by_role("button", name="Download data")
        download_button.wait_for(state="visible", timeout=30000)
        with page.expect_download() as download_info:
            download_button.click()
        download = download_info.value
        print(f"Suggested filename: {download.suggested_filename}")
        download_path = os.path.join(downloads_dir, f"{int(time.time())}_{download.suggested_filename}")
        download.save_as(download_path)
        time.sleep(2)
        if not os.path.exists(download_path):
            print(f"WARNING: File not found after download: {download_path}")
            failed_urls.append(url)
        else:
            print(f"Downloaded file saved to: {download_path}")
    except Exception as e:
        print(f"ERROR: Download failed: {e}")
        failed_urls.append(url)
        continue

    print(f"Finished processing: {url}")

# After the loop, report failed URLs
if failed_urls:
    print("\nThe following links failed to scrape and were skipped:")
    for bad_url in failed_urls:
        print(bad_url)
    failed_links_path = os.path.join(downloads_dir, "scrape_failed_links.txt")
    with open(failed_links_path, "w", encoding="utf-8") as f:
        for bad_url in failed_urls:
            f.write(bad_url + "\n")
    print(f"Failed links saved to: {failed_links_path}")
else:
    print("\nAll links scraped successfully.")



# Optionally combine data or perform post-processing
# scp.combine_data(...)
time.sleep(600)
browser.close()