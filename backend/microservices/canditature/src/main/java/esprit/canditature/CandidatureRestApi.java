package esprit.canditature;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("/mic3/candidature")
public class CandidatureRestApi {

    private final CandidatureRepository repository;

    public CandidatureRestApi(CandidatureRepository repository) {
        this.repository = repository;
    }

    @GetMapping("/hello")
    public String sayHello() {
        return "Hello Im microservice 3!";
    }

    @GetMapping
    public List<Candidature> lister() {
        return repository.findAll();
    }

    @GetMapping("/{id}")
    public Candidature afficher(@PathVariable Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(
                        HttpStatus.NOT_FOUND, "Candidature introuvable"));
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Candidature creer(@Valid @RequestBody Creation demande) {
        return repository.save(
                new Candidature(demande.candidatId(), demande.jobId()));
    }

    @PutMapping("/{id}")
    public Candidature modifier(
            @PathVariable Long id, @Valid @RequestBody Modification demande) {
        Candidature candidature = afficher(id);
        candidature.modifier(demande.candidatId(), demande.jobId(), demande.statut());
        return repository.save(candidature);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void supprimer(@PathVariable Long id) {
        repository.delete(afficher(id));
    }

    public record Creation(
            @NotNull @Positive Long candidatId,
            @NotNull @Positive Long jobId) {
    }

    public record Modification(
            @NotNull @Positive Long candidatId,
            @NotNull @Positive Long jobId,
            @NotNull Candidature.Statut statut) {
    }
}