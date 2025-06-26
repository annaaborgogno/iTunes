from database.DB_connect import DBConnect
from model.album import Album


class DAO():

   @staticmethod
   def getAlbums(dMin):
       cnx = DBConnect.get_connection()
       cursor = cnx.cursor(dictionary=True)
       query="""select a.*, sum(t.Milliseconds)/1000/60 as dTot
                from album a, track t 
                where a.AlbumId = t.AlbumId
                group by a.AlbumId
                having dTot > %s"""
       cursor.execute(query, (dMin, )) # in minuti

       res = []
       for row in cursor:
           res.append(Album(**row)) #i nomi sono uguali quindi faccio l'unpack della lista
       cursor.close()
       cnx.close()
       return res

   @staticmethod
   def getAllEdges(idMapAlbum):
       cnx = DBConnect.get_connection()
       cursor = cnx.cursor(dictionary=True)
       #distinctrow identifica una riga univoca per ogni coppia di album
       query = """select distinctrow t1.AlbumId as a1, t2.AlbumId as a2
                    from track t1, track t2, playlisttrack p1, playlisttrack p2
                    where t1.TrackId = p1.TrackId and t2.TrackId = p2.TrackId 
                    and p1.PlaylistId = p2.PlaylistId
                    and t1.AlbumId < t2.AlbumId"""
       cursor.execute(query)

       res = []
       for row in cursor:
           # tuple di nodi, che costituiscono tutti gli archi possibili, filtriamo poi i nodi che esistono
           if row["a1"] in idMapAlbum and row["a2"] in idMapAlbum:
               res.append((idMapAlbum[row["a1"]], idMapAlbum[row["a2"]]))
       cursor.close() #chiudere sempre le connessioni perché altrimenti si esaurisce il pool di connessioni
       cnx.close()
       return res